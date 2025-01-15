from typing import Any, Generator

from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse

from backend.config.routers import RouterName
from backend.database_models.database import DBSessionDep
from backend.model_deployments import TGIDeployment
from backend.schemas.chat import ChatResponseEvent, SalonChatRequest
from backend.services.auth.utils import get_header_user_id
from backend.services.chat import (
    generate_chat_stream,
    process_chat,
)

router = APIRouter(
    prefix="/v1",
)
router.name = RouterName.CHAT  # type: ignore


@router.post("/chat-stream")
async def chat_stream(
    session: DBSessionDep,
    chat_request: SalonChatRequest,
    request: Request,
    user_id: str = Depends(get_header_user_id),
) -> Generator[
    ChatResponseEvent, Any, None
]:  # so that openapi can generate the schema, is there a better way?
    """
    Stream chat endpoint to handle user messages and return chatbot responses.

    Args:
        session (DBSessionDep): Database session.
        chat_request (CohereChatRequest): Chat request data.
        request (Request): Request object.

    Returns:
        EventSourceResponse: Server-sent event response with chatbot responses.
    """
    print(f"Description {chat_request.description}")
    (
        session,
        chat_request,
        response_message,
        should_store,
        next_message_position,
    ) = process_chat(session, chat_request, request, user_id)

    return EventSourceResponse(  # type: ignore
        generate_chat_stream(
            session,
            TGIDeployment().invoke_chat_stream(chat_request),
            response_message,
            should_store=should_store,
            next_message_position=next_message_position,
            conversation_id=chat_request.conversation_id,
            user_id=user_id,
        ),
        media_type="text/event-stream",
        headers={"Connection": "keep-alive"},
        send_timeout=300,
        ping=5,
    )
