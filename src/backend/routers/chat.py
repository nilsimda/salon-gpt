from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

from backend.config.routers import RouterName
from backend.database_models.database import DBSessionDep
from backend.model_deployments import TGIDeployment
from backend.schemas.chat import (
    BaseChatRequest,
    SearchChatRequest,
)
from backend.services.chat import (
    generate_chat_stream,
    process_chat,
    process_message_regeneration,
)

router = APIRouter(
    prefix="/v1",
)
router.name = RouterName.CHAT


@router.post("/chat-stream")
async def chat_stream(
    session: DBSessionDep,
    chat_request: BaseChatRequest,
    request: Request,
) -> EventSourceResponse:
    """
    Stream chat endpoint to handle user messages and return chatbot responses.

    Args:
        session (DBSessionDep): Database session.
        chat_request (CohereChatRequest): Chat request data.
        request (Request): Request object.
        ctx (Context): Context object.

    Returns:
        EventSourceResponse: Server-sent event response with chatbot responses.
    """

    (
        session,
        chat_request,
        response_message,
        should_store,
        next_message_position,
    ) = process_chat(session, chat_request, request)

    return EventSourceResponse(
        generate_chat_stream(
            session,
            TGIDeployment().invoke_chat_stream(chat_request),
            response_message,
            should_store=should_store,
            next_message_position=next_message_position,
        ),
        media_type="text/event-stream",
        headers={"Connection": "keep-alive"},
        send_timeout=300,
        ping=5,
    )


@router.post("/chat-stream/regenerate")
async def regenerate_chat_stream(
    session: DBSessionDep,
    chat_request: BaseChatRequest,
    request: Request,
) -> EventSourceResponse:
    """
    Endpoint to regenerate stream chat response for the last user message.

    Args:
        session (DBSessionDep): Database session.
        chat_request (CohereChatRequest): Chat request data.
        request (Request): Request object.
        ctx (Context): Context object.

    Returns:
        EventSourceResponse: Server-sent event response with chatbot responses.
    """
    (
        session,
        chat_request,
        new_response_message,
        previous_response_message_ids,
    ) = process_message_regeneration(session, chat_request, request)

    return EventSourceResponse(
        generate_chat_stream(
            session,
            TGIDeployment().invoke_chat_stream(chat_request),
            new_response_message,
            next_message_position=new_response_message.position,
            previous_response_message_ids=previous_response_message_ids,
        ),
        media_type="text/event-stream",
        headers={"Connection": "keep-alive"},
        send_timeout=300,
        ping=5,
    )


@router.post("/search-stream")
async def search_stream(
    session: DBSessionDep,
    search_request: SearchChatRequest,
    request: Request,
) -> EventSourceResponse:
    """
    Stream search endpoint to handle user messages and return search result responses.

    Args:
        session (DBSessionDep): Database session.
        search_request (SearchChatRequest): Search request data.
        request (Request): Request object.
        ctx (Context): Context object.

    Returns:
        EventSourceResponse: Server-sent event response with chatbot responses.
    """

    (
        session,
        search_request,
        response_message,
        should_store,
        next_message_position,
    ) = process_chat(session, search_request, request)

    return EventSourceResponse(
        generate_chat_stream(
            session,
            TGIDeployment().invoke_search_stream(
                search_request,
            ),
            response_message,
            should_store=should_store,
            next_message_position=next_message_position,
        ),
        media_type="application/json",
        headers={"Connection": "keep-alive"},
        send_timeout=300,
        ping=5,
    )
