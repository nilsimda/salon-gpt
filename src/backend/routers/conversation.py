from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi import File as RequestFile
from fastapi import UploadFile as FastAPIUploadFile

from backend.config.routers import RouterName
from backend.crud import conversation as conversation_crud
from backend.database_models import Conversation as ConversationModel
from backend.database_models.database import DBSessionDep
from backend.schemas.conversation import (
    Conversation,
    ConversationWithoutMessages,
    DeleteConversationResponse,
    GenerateTitleResponse,
    ToggleConversationPinRequest,
    UpdateConversationRequest,
)
from backend.services.conversation import (
    filter_conversations,
    generate_conversation_title,
    get_documents_to_rerank,
    get_messages_with_files,
    validate_conversation,
)

router = APIRouter(
    prefix="/v1/conversations",
)
router.name = RouterName.CONVERSATION


# CONVERSATIONS
@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: str,
    user_id: str,
    session: DBSessionDep,
    request: Request,
) -> Conversation:
    """
    Get a conversation by ID.

    Args:
        conversation_id (str): Conversation ID.
        session (DBSessionDep): Database session.
        request (Request): Request object.

    Returns:
        Conversation: Conversation with the given ID.

    Raises:
        HTTPException: If the conversation with the given ID is not found.
    """
    conversation = conversation_crud.get_conversation(session, conversation_id, user_id)

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail=f"Conversation with ID: {conversation_id} not found.",
        )

    messages = get_messages_with_files(session, user_id, conversation.messages)
    _ = validate_conversation(session, conversation_id, user_id)

    conversation = Conversation(
        id=conversation.id,
        user_id=user_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        title=conversation.title,
        messages=messages,
        description=conversation.description,
        agent_id=conversation.agent_id,
        is_pinned=conversation.is_pinned,
    )

    _ = validate_conversation(session, conversation_id, user_id)
    return conversation


@router.get("", response_model=list[ConversationWithoutMessages])
async def list_conversations(
    *,
    offset: int = 0,
    limit: int = 100,
    order_by: Optional[str] = None,
    agent_id: Optional[str] = None,
    session: DBSessionDep,
    request: Request,
) -> list[ConversationWithoutMessages]:
    """
    List all conversations.

    Args:
        offset (int): Offset to start the list.
        limit (int): Limit of conversations to be listed.
        order_by (str): A field by which to order the conversations.
        agent_id (str): Query parameter for agent ID to optionally filter conversations by agent.
        session (DBSessionDep): Database session.
        request (Request): Request object.

    Returns:
        list[ConversationWithoutMessages]: List of conversations.
    """
    user_id = ctx.get_user_id()

    conversations = conversation_crud.get_conversations(
        session,
        offset=offset,
        limit=limit,
        order_by=order_by,
        user_id=user_id,
        agent_id=agent_id,
    )

    results = []
    for conversation in conversations:
        results.append(
            ConversationWithoutMessages(
                id=conversation.id,
                user_id=user_id,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at,
                title=conversation.title,
                description=conversation.description,
                agent_id=conversation.agent_id,
                messages=[],
                is_pinned=conversation.is_pinned,
            )
        )

    return results


@router.put("/{conversation_id}", response_model=Conversation)
async def update_conversation(
    conversation_id: str,
    user_id: str,
    new_conversation: UpdateConversationRequest,
    session: DBSessionDep,
) -> Conversation:
    """
    Update a conversation by ID.

    Args:
        conversation_id (str): Conversation ID.
        new_conversation (UpdateConversationRequest): New conversation data.
        session (DBSessionDep): Database session.

    Returns:
        Conversation: Updated conversation.

    Raises:
        HTTPException: If the conversation with the given ID is not found.
    """
    conversation = validate_conversation(session, conversation_id, user_id)
    conversation = conversation_crud.update_conversation(
        session, conversation, new_conversation
    )

    messages = get_messages_with_files(session, user_id, conversation.messages)
    return Conversation(
        id=conversation.id,
        user_id=user_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        title=conversation.title,
        messages=messages,
        description=conversation.description,
        agent_id=conversation.agent_id,
        is_pinned=conversation.is_pinned,
    )


@router.put("/{conversation_id}/toggle-pin", response_model=ConversationWithoutMessages)
async def toggle_conversation_pin(
    conversation_id: str,
    user_id: str,
    new_conversation_pin: ToggleConversationPinRequest,
    session: DBSessionDep,
) -> ConversationWithoutMessages:
    conversation = validate_conversation(session, conversation_id, user_id)
    conversation = conversation_crud.toggle_conversation_pin(
        session, conversation, new_conversation_pin
    )
    return ConversationWithoutMessages(
        id=conversation.id,
        user_id=user_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        title=conversation.title,
        description=conversation.description,
        agent_id=conversation.agent_id,
        messages=[],
        is_pinned=conversation.is_pinned,
    )


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str, user_id: str, session: DBSessionDep
) -> DeleteConversationResponse:
    """
    Delete a conversation by ID.

    Args:
        conversation_id (str): Conversation ID.
        session (DBSessionDep): Database session.
        ctx (Context): Context object.

    Returns:
        DeleteConversationResponse: Empty response.

    Raises:
        HTTPException: If the conversation with the given ID is not found.
    """
    conversation = validate_conversation(session, conversation_id, user_id)

    conversation_crud.delete_conversation(session, conversation_id, user_id)

    return DeleteConversationResponse()


@router.get(":search", response_model=list[ConversationWithoutMessages])
async def search_conversations(
    query: str,
    user_id: str,
    session: DBSessionDep,
    request: Request,
    offset: int = 0,
    limit: int = 100,
    agent_id: Optional[str] = None,
) -> list[ConversationWithoutMessages]:
    """
    Search conversations by title.

    Args:
        query (str): Query string to search for in conversation titles.
        session (DBSessionDep): Database session.
        request (Request): Request object.
        offset (int): Offset to start the list.
        limit (int): Limit of conversations to be listed.
        agent_id (str): Query parameter for agent ID to optionally filter conversations by agent.
        ctx (Context): Context object.

    Returns:
        list[ConversationWithoutMessages]: List of conversations that match the query.
    """

    conversations = conversation_crud.get_conversations(
        session, offset=offset, limit=limit, user_id=user_id, agent_id=agent_id
    )

    if not conversations:
        return []

    rerank_documents = get_documents_to_rerank(conversations)
    filtered_documents = await filter_conversations(
        query,
        conversations,
        rerank_documents,
        ctx,
    )

    results = []
    for conversation in filtered_documents:
        results.append(
            ConversationWithoutMessages(
                id=conversation.id,
                user_id=user_id,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at,
                title=conversation.title,
                description=conversation.description,
                agent_id=conversation.agent_id,
                messages=[],
                is_pinned=conversation.is_pinned,
            )
        )
    return results


# MISC
@router.post("/{conversation_id}/generate-title", response_model=GenerateTitleResponse)
async def generate_title(
    conversation_id: str,
    user_id: str,
    session: DBSessionDep,
    request: Request,
    model: Optional[str] = "command-r",
) -> GenerateTitleResponse:
    """
    Generate a title for a conversation and update the conversation with the generated title.

    Args:
        conversation_id (str): Conversation ID.
        session (DBSessionDep): Database session.
        request (Request): Request object.
        ctx (Context): Context object.

    Returns:
        str: Generated title for the conversation.

    Raises:
        HTTPException: If the conversation with the given ID is not found.
    """

    conversation = validate_conversation(session, conversation_id, user_id)
    agent_id = conversation.agent_id if conversation.agent_id else None

    title, error = await generate_conversation_title(
        session,
        conversation,
        user_id,
        agent_id,
        model,
    )

    conversation_crud.update_conversation(
        session, conversation, UpdateConversationRequest(title=title)
    )

    return GenerateTitleResponse(
        title=title,
        error=error,
    )
