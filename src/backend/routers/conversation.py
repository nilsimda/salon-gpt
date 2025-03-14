from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import parse_obj_as

from backend.config.routers import RouterName
from backend.crud import conversation as conversation_crud
from backend.database_models.database import DBSessionDep
from backend.schemas.conversation import (
    Conversation,
    ConversationWithoutMessages,
    DeleteConversationResponse,
    GenerateTitleResponse,
    ToggleConversationPinRequest,
    UpdateConversationRequest,
)
from backend.services.auth.utils import get_header_user_id
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
router.name = RouterName.CONVERSATION  # type: ignore


# CONVERSATIONS
@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: str,
    session: DBSessionDep,
    request: Request,
    user_id: str = Depends(get_header_user_id),
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
    user_id: str = Depends(get_header_user_id),
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
    new_conversation: UpdateConversationRequest,
    session: DBSessionDep,
    request: Request,
    user_id: str = Depends(get_header_user_id),
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
    new_conversation_pin: ToggleConversationPinRequest,
    session: DBSessionDep,
    request: Request,
    user_id: str = Depends(get_header_user_id),
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
    conversation_id: str,
    session: DBSessionDep,
    request: Request,
    user_id: str = Depends(get_header_user_id),
) -> DeleteConversationResponse:
    """
    Delete a conversation by ID.

    Args:
        conversation_id (str): Conversation ID.
        session (DBSessionDep): Database session.

    Returns:
        DeleteConversationResponse: Empty response.

    Raises:
        HTTPException: If the conversation with the given ID is not found.
    """
    validate_conversation(session, conversation_id, user_id)

    conversation_crud.delete_conversation(session, conversation_id, user_id)

    return DeleteConversationResponse()


@router.get(":search", response_model=list[ConversationWithoutMessages])
async def search_conversations(
    query: str,
    session: DBSessionDep,
    request: Request,
    offset: int = 0,
    limit: int = 100,
    agent_id: Optional[str] = None,
    user_id: str = Depends(get_header_user_id),
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
          (Context): Context object.

    Returns:
        list[ConversationWithoutMessages]: List of conversations that match the query.
    """

    conversations = conversation_crud.get_conversations(
        session, offset=offset, limit=limit, user_id=user_id, agent_id=agent_id
    )

    if not conversations:
        return []
    conversations = parse_obj_as(list[Conversation], conversations)

    rerank_documents = get_documents_to_rerank(conversations)
    filtered_documents = await filter_conversations(
        query,
        conversations,
        rerank_documents,
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
    session: DBSessionDep,
    request: Request,
    user_id: str = Depends(get_header_user_id),
) -> GenerateTitleResponse:
    """
    Generate a title for a conversation and update the conversation with the generated title.

    Args:
        conversation_id (str): Conversation ID.
        session (DBSessionDep): Database session.
        request (Request): Request object.
          (Context): Context object.

    Returns:
        str: Generated title for the conversation.

    Raises:
        HTTPException: If the conversation with the given ID is not found.
    """

    conversation = validate_conversation(session, conversation_id, user_id)

    title, error = await generate_conversation_title(
        session,
        parse_obj_as(Conversation, conversation),
        user_id,
    )

    conversation_crud.update_conversation(
        session, conversation, UpdateConversationRequest(title=title)
    )

    return GenerateTitleResponse(
        title=title,
        error=error,
    )
