from fastapi import HTTPException, Request

import backend.crud.user as user_crud
from backend.crud import conversation as conversation_crud
from backend.crud import study as study_crud
from backend.database_models.database import DBSessionDep
from backend.services.auth.utils import get_header_user_id


def validate_user_header(session: DBSessionDep, request: Request):
    """
    Validate that the request has the `User-Id` header, used for requests
    that require a User.

    Args:
        request (Request): The request to validate

    Raises:
        HTTPException: If no `User-Id` header.

    """

    user_id = get_header_user_id(request)
    if not user_id:
        print("User-Id required in request headers.")
        raise HTTPException(
            status_code=401, detail="User-Id required in request headers."
        )

    user = user_crud.get_user(session, user_id)
    if not user:
        print(f"User {user_id} not found.")
        raise HTTPException(status_code=401, detail="User not found.")


async def validate_chat_request(session: DBSessionDep, request: Request):
    """
    Validate that the request has the appropriate values in the body

    Args:
        request (Request): The request to validate

    Raises:
        HTTPException: If the request does not have the appropriate values in the body
    """
    # Validate that the agent_id is valid
    body = await request.json()
    user_id = get_header_user_id(request)

    agent_id = request.query_params.get("agent_id")

    # If conversation_id is passed in with agent_id, then make sure that conversation exists with the agent_id
    conversation_id = body.get("conversation_id")
    if conversation_id and agent_id:
        conversation = conversation_crud.get_conversation(
            session, conversation_id, user_id
        )
        if conversation is None or conversation.agent_id != agent_id:
            raise HTTPException(
                status_code=404,
                detail=f"Conversation ID {conversation_id} not found for specified agent.",
            )


async def validate_create_study_request(session: DBSessionDep, request: Request):
    """
    Validate that the create study request is valid.

    Args:
        session (DBSessionDep): Database session.
        request (Request): The request to validate

    Raises:
        HTTPException: If the request does not have the appropriate values in the body
    """
    user_id = get_header_user_id(request)
    body = await request.json()

    # Validate required fields
    name = body.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Study name is required.")

    # Check if study with same name exists for user
    study = study_crud.get_study_by_name(session, name, user_id=user_id)
    if study:
        raise HTTPException(status_code=400, detail=f"Study {name} already exists.")


async def validate_update_study_request(session: DBSessionDep, request: Request):
    """
    Validate that the update study request is valid.

    Args:
        session (DBSessionDep): Database session.
        request (Request): The request to validate

    Raises:
        HTTPException: If the request does not have the appropriate values in the body
    """
    user_id = get_header_user_id(request)
    study_id = request.path_params.get("study_id")
    if not study_id:
        raise HTTPException(status_code=400, detail="Study ID is required.")

    study = study_crud.get_study_by_id(session, study_id, user_id)
    if not study:
        raise HTTPException(
            status_code=404, detail=f"Study with ID {study_id} not found."
        )

    if study.user_id != user_id:
        raise HTTPException(
            status_code=401, detail=f"Study with ID {study_id} does not belong to user."
        )

    body = await request.json()
    name = body.get("name")
    if name:
        existing_study = study_crud.get_study_by_name(session, name, user_id=user_id)
        if existing_study and existing_study.id != study_id:
            raise HTTPException(
                status_code=400, detail=f"Study with name {name} already exists."
            )
