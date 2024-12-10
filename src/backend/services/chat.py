import json
from typing import Any, AsyncGenerator, Generator, Optional
from uuid import uuid4

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder

from backend.crud import conversation as conversation_crud
from backend.crud import message as message_crud
from backend.database_models.conversation import Conversation
from backend.database_models.database import DBSessionDep
from backend.database_models.message import (
    Message,
    MessageAgent,
)
from backend.schemas import BaseChatRequest
from backend.schemas.chat import (
    ChatMessage,
    ChatResponseEvent,
    ChatRole,
    StreamEnd,
    StreamEvent,
    StreamEventType,
    StreamStart,
    StreamTextGeneration,
)
from backend.schemas.conversation import UpdateConversationRequest


def process_chat(
    session: DBSessionDep,
    chat_request: BaseChatRequest,
    request: Request,
) -> tuple[DBSessionDep, BaseChatRequest, Message, bool, int]:
    """
    Process a chat request.

    Args:
        chat_request (BaseChatRequest): Chat request data.
        session (DBSessionDep): Database session.
        request (Request): Request object.

    Returns:
        Tuple: Tuple containing necessary data to construct the responses.
    """
    user_id = chat_request.user_id
    agent_id = chat_request.agent_id

    should_store = chat_request.chat_history is None
    conversation = get_or_create_conversation(
        session,
        chat_request,
        user_id,
        should_store,
        agent_id,
        chat_request.message,
    )

    # Get position to put next message in
    next_message_position = get_next_message_position(conversation)

    # store user message
    create_message(
        session,
        chat_request,
        conversation.id,
        user_id,
        next_message_position,
        chat_request.message,
        MessageAgent.USER,
        should_store,
        id=str(uuid4()),
    )

    # store chatbot message
    chatbot_message = create_message(
        session,
        chat_request,
        conversation.id,
        user_id,
        next_message_position,
        "",
        MessageAgent.CHATBOT,
        False,
        id=str(uuid4()),
    )

    chat_history = create_chat_history(
        conversation, next_message_position, chat_request
    )

    chat_request.chat_history = chat_history

    return (
        session,
        chat_request,
        chatbot_message,
        should_store,
        next_message_position,
    )


def get_last_message(
    conversation: Conversation, user_id: str, agent: MessageAgent
) -> Message:
    """
    Retrieve the last message sent by a specific agent within a given conversation.

    Args:
        conversation (Conversation): The conversation containing the messages.
        user_id (str): The user ID.
        agent (MessageAgent): The agent whose last message is to be retrieved.

    Returns:
        Message: The last message sent by the agent.

    Raises:
        HTTPException: If there are no messages from the specified agent in the conversation.
    """
    agent_messages = [
        message
        for message in conversation.messages
        if message.is_active and message.user_id == user_id and message.agent == agent
    ]

    if not agent_messages:
        raise HTTPException(
            status_code=404,
            detail=f"Messages for user with ID: {user_id} not found.",
        )

    return agent_messages[-1]


def get_or_create_conversation(
    session: DBSessionDep,
    chat_request: BaseChatRequest,
    user_id: str,
    should_store: bool,
    agent_id: str | None = None,
    user_message: str = "",
) -> Conversation:
    """
    Gets or creates a Conversation based on the chat request.

    Args:
        session (DBSessionDep): Database session.
        chat_request (BaseChatRequest): Chat request data.
        user_id (str): User ID.
        should_store (bool): Whether to store the conversation in the database.

    Returns:
        Conversation: Conversation object.
    """
    conversation_id = chat_request.conversation_id or ""
    conversation = conversation_crud.get_conversation(session, conversation_id, user_id)
    if conversation is None:
        # Get the first 5 words of the user message as the title
        title = " ".join(user_message.split()[:5])

        conversation = Conversation(
            user_id=user_id,
            id=chat_request.conversation_id,
            agent_id=agent_id,
            title=title,
        )

        if should_store:
            conversation_crud.create_conversation(session, conversation)

    return conversation


def get_next_message_position(conversation: Conversation) -> int:
    """
    Gets message position to create next messages.

    Args:
        conversation (Conversation): current Conversation.

    Returns:
        int: Position to save new messages with
    """

    # Message starts the conversation
    if len(conversation.messages) == 0:
        return 0

    # Get current max position from existing Messages
    current_active_position = max(
        [message.position for message in conversation.messages if message.is_active]
    )

    return current_active_position + 1


def create_message(
    session: DBSessionDep,
    chat_request: BaseChatRequest,
    conversation_id: str,
    user_id: str,
    user_message_position: int,
    text: str | None = None,
    agent: MessageAgent = MessageAgent.USER,
    should_store: bool = True,
    id: str | None = None,
) -> Message:
    """
    Create a message object and store it in the database.

    Args:
        session (DBSessionDep): Database session.
        chat_request (BaseChatRequest): Chat request data.
        conversation_id (str): Conversation ID.
        user_id (str): User ID.
        user_message_position (int): User message position.
        id (str): Message ID.
        text (str): Message text.
        agent (MessageAgent): Message agent.
        should_store (bool): Whether to store the message in the database.

    Returns:
        Message: Message object.
    """
    if not id:
        id = str(uuid4())

    message = Message(
        id=id,
        user_id=user_id,
        conversation_id=conversation_id,
        text=text,
        position=user_message_position,
        is_active=True,
        agent=agent,
    )

    if should_store:
        return message_crud.create_message(session, message)
    return message


def create_chat_history(
    conversation: Conversation,
    user_message_position: int,
    chat_request: BaseChatRequest,
) -> list[ChatMessage]:
    """
    Create chat history from conversation messages or request.

    Args:
        conversation (Conversation): Conversation object.
        user_message_position (int): User message position.
        chat_request (BaseChatRequest): Chat request data.

    Returns:
        list[ChatMessage]: List of chat messages.
    """
    if chat_request.chat_history is not None:
        return chat_request.chat_history

    if conversation.messages is None:
        return []

    # Don't include the user message that was just sent
    text_messages = [
        message
        for message in conversation.messages
        if message.position < user_message_position
    ]
    return [
        ChatMessage(
            role=ChatRole(message.agent.value.upper()),
            message=message.text,
        )
        for message in text_messages
    ]


def update_conversation_after_turn(
    session: DBSessionDep,
    response_message: Message,
    conversation_id: str,
    final_message_text: str,
    user_id: str,
    previous_response_message_ids: list[str] | None = None,
) -> None:
    """
    After the last message in a conversation, updates the conversation description with that message's text

    Args:
        session (DBSessionDep): Database session.
        response_message (Message): Response message object.
        conversation_id (str): Conversation ID.
        final_message_text (str): Final message text.
        user_id (str): The user ID.
        previous_response_message_ids (list[str]): Previous response message IDs.
    """
    if previous_response_message_ids:
        message_crud.delete_messages(session, previous_response_message_ids, user_id)

    message_crud.create_message(session, response_message)

    # Update conversation description with final message
    conversation = conversation_crud.get_conversation(session, conversation_id, user_id)
    new_conversation = UpdateConversationRequest(
        description=final_message_text,
        user_id=conversation.user_id,
    )
    conversation_crud.update_conversation(session, conversation, new_conversation)


async def generate_chat_response(
    session: DBSessionDep,
    model_deployment_stream: AsyncGenerator[Any, Any],
    response_message: Message,
    should_store: bool = True,
    **kwargs: Any,
) -> Optional[StreamEnd]:
    """
    Generate chat response from model deployment non streaming response.
    Use the stream to generate the response and all the intermediate steps, then
    return only the final step as a non-streamed response.

    Args:
        session (DBSessionDep): Database session.
        model_deployment_stream (AsyncGenerator[Any, Any]): Model deployment stream.
        response_message (Message): Response message object.
        should_store (bool): Whether to store the conversation in the database.
          (Context): Context object.
        **kwargs (Any): Additional keyword arguments.

    Yields:
        bytes: Byte representation of chat response event.
    """
    stream = generate_chat_stream(
        session,
        model_deployment_stream,
        response_message,
        should_store,
        **kwargs,
    )

    non_streamed_chat_response = None
    async for event in stream:
        event = json.loads(event)
        if event["event"] == StreamEvent.STREAM_END:
            data = event["data"]
            generation_id = response_message.generation_id if response_message else None

            non_streamed_chat_response = StreamEnd(
                text=data.get("text", ""),
                generation_id=generation_id,
                chat_history=data.get("chat_history", []),
                finish_reason=data.get("finish_reason", ""),
                error=data.get("error", None),
            )

    return non_streamed_chat_response


async def generate_chat_stream(
    session: DBSessionDep,
    model_deployment_stream: AsyncGenerator[Any, Any],
    response_message: Message,
    should_store: bool = True,
    user_id: str = "",
    conversation_id: str = "",
    **kwargs: Any,
) -> AsyncGenerator[Any, Any]:
    """
    Generate chat stream from model deployment stream.

    Args:
        session (DBSessionDep): Database session.
        model_deployment_stream (AsyncGenerator[Any, Any]): Model deployment stream.
        response_message (Message): Response message object.
        conversation_id (str): Conversation ID.
        user_id (str): User ID.
        should_store (bool): Whether to store the conversation in the database.
          (Context): Context object.
        **kwargs (Any): Additional keyword arguments.

    Yields:
        bytes: Byte representation of chat response event.
    """

    stream_end_data = {
        "message_id": response_message.id,
        "conversation_id": conversation_id,
        "text": "",
    }

    stream_event = None
    async for event in model_deployment_stream:
        (
            stream_event,
            stream_end_data,
            response_message,
        ) = handle_stream_event(
            event,
            conversation_id,
            stream_end_data,
            response_message,
            session=session,
            should_store=should_store,
            user_id=user_id,
            next_message_position=kwargs.get("next_message_position", 0),
        )

        print(stream_event)

        yield json.dumps(
            jsonable_encoder(
                ChatResponseEvent(
                    event=stream_event.event_type.value,
                    data=stream_event,
                )
            )
        )

    if should_store:
        update_conversation_after_turn(
            session,
            response_message,
            conversation_id,
            stream_end_data["text"],
            user_id,
            kwargs.get("previous_response_message_ids"),
        )


def handle_stream_event(
    event: dict[str, Any],
    conversation_id: str,
    stream_end_data: dict[str, Any],
    response_message: Message,
    session: DBSessionDep,
    should_store: bool = True,
    user_id: str = "",
    next_message_position: int = 0,
) -> tuple[StreamEventType, dict[str, Any], Message]:
    handlers = {
        StreamEvent.STREAM_START: handle_stream_start,
        StreamEvent.TEXT_GENERATION: handle_stream_text_generation,
        StreamEvent.STREAM_END: handle_stream_end,
    }
    event_type = event["event_type"]

    return handlers[event_type](
        event,
        conversation_id,
        stream_end_data,
        response_message,
        session=session,
        should_store=should_store,
        user_id=user_id,
        next_message_position=next_message_position,
    )


def handle_stream_start(
    event: dict[str, Any],
    conversation_id: str,
    stream_end_data: dict[str, Any],
    response_message: Message,
    **kwargs: Any,
) -> tuple[StreamStart, dict[str, Any], Message]:
    event["conversation_id"] = conversation_id
    stream_event = StreamStart.model_validate(event)
    if response_message:
        response_message.generation_id = event["generation_id"]
    stream_end_data["generation_id"] = event["generation_id"]
    return stream_event, stream_end_data, response_message


def handle_stream_text_generation(
    event: dict[str, Any],
    _: str,
    stream_end_data: dict[str, Any],
    response_message: Message,
    **kwargs: Any,
) -> tuple[StreamTextGeneration, dict[str, Any], Message]:
    stream_end_data["text"] += event["text"]
    stream_event = StreamTextGeneration.model_validate(event)
    return stream_event, stream_end_data, response_message


def to_dict(obj):
    return json.loads(
        json.dumps(
            obj, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o)
        )
    )


def handle_stream_end(
    event: dict[str, Any],
    _: str,
    stream_end_data: dict[str, Any],
    response_message: Message,
    **kwargs: Any,
) -> tuple[StreamEnd, dict[str, Any], Message]:
    if response_message:
        response_message.text = stream_end_data["text"]

    stream_end_data["chat_history"] = (
        to_dict(event).get("response", {}).get("chat_history", [])
    )
    stream_end = StreamEnd.model_validate(event | stream_end_data)
    stream_event = stream_end
    return stream_event, stream_end_data, response_message
