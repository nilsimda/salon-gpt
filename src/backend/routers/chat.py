from typing import Any, Generator

from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse

from backend.config.routers import RouterName
from backend.database_models.database import DBSessionDep
from backend.model_deployments import TGIDeployment
from backend.schemas.chat import (
    BaseChatRequest,
    ChatResponseEvent,
)
from backend.schemas.context import Context
from backend.services.chat import (
    generate_chat_stream,
    process_chat,
    process_message_regeneration,
)
from backend.services.context import get_context

router = APIRouter(
    prefix="/v1",
)
router.name = RouterName.CHAT


@router.post("/chat-stream")
async def chat_stream(
    session: DBSessionDep,
    chat_request: BaseChatRequest,
    request: Request,
    ctx: Context = Depends(get_context),
) -> Generator[ChatResponseEvent, Any, None]:
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

    #ctx.with_model(chat_request.model)
    #agent_id = chat_request.agent_id
    #ctx.with_agent_id(agent_id)

    (
        session,
        chat_request,
        response_message,
        should_store,
        next_message_position,
        ctx,
    ) = process_chat(session, chat_request, request, ctx)

    return EventSourceResponse(
        generate_chat_stream(
            session,
            TGIDeployment().invoke_chat_stream(
                chat_request,
                ctx,
            ),
            response_message,
            should_store=should_store,
            next_message_position=next_message_position,
            ctx=ctx,
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
    ctx: Context = Depends(get_context),
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
    ctx.with_model(chat_request.model)

    agent_id = chat_request.agent_id
    ctx.with_agent_id(agent_id)

    (
        session,
        chat_request,
        new_response_message,
        previous_response_message_ids,
        managed_tools,
        ctx,
    ) = process_message_regeneration(session, chat_request, request, ctx)

    return EventSourceResponse(
        generate_chat_stream(
            session,
            TGIDeployment().invoke_chat_stream(
                chat_request,
                ctx,
            ),
            new_response_message,
            next_message_position=new_response_message.position,
            previous_response_message_ids=previous_response_message_ids,
            ctx=ctx,
        ),
        media_type="text/event-stream",
        headers={"Connection": "keep-alive"},
        send_timeout=300,
        ping=5,
    )
