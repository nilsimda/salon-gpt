from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from backend.config.routers import RouterName
from backend.crud import study as study_crud
from backend.database_models.database import DBSessionDep
from backend.database_models.study import Study as StudyModel
from backend.schemas.context import Context
from backend.schemas.study import (
    CreateStudyRequest,
    DeleteStudy,
    Study,
    StudyPublic,
    UpdateStudyRequest,
)
from backend.services.context import get_context
from backend.services.request_validators import (
    validate_create_study_request,
    validate_update_study_request,
    validate_user_header,
)
from backend.services.study import (
    raise_db_error,
    validate_study_exists,
)

router = APIRouter(
    prefix="/v1/studies",
)
router.name = RouterName.STUDY

@router.post(
    "",
    response_model=StudyPublic,
    dependencies=[
        Depends(validate_user_header),
        Depends(validate_create_study_request),
    ],
)
async def create_study(
    session: DBSessionDep,
    study: CreateStudyRequest,
    ctx: Context = Depends(get_context),
) -> StudyPublic:
    """
    Create a study.

    Args:
        session (DBSessionDep): Database session.
        study (CreateStudyRequest): Study data.
        ctx (Context): Context object.
    Returns:
        StudyPublic: Created study with no user ID or organization ID.
    Raises:
        HTTPException: If the study creation fails.
    """
    ctx.with_user(session)
    user_id = ctx.get_user_id()
    logger = ctx.get_logger()

    study_data = StudyModel(
        name=study.name,
        individual_interview_count=study.individual_interview_count,
        group_interview_count=study.group_interview_count,
        user_id=user_id,
        organization_id=study.organization_id,
    )

    try:
        created_study = study_crud.create_study(session, study_data)
        study_schema = Study.model_validate(created_study)
        ctx.with_study(study_schema)
        return created_study
    except Exception as e:
        logger.exception(event=e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=list[StudyPublic])
async def list_studies(
    *,
    offset: int = 0,
    limit: int = 100,
    session: DBSessionDep,
    organization_id: Optional[str] = None,
    ctx: Context = Depends(get_context),
) -> list[StudyPublic]:
    """
    List all studies.

    Args:
        offset (int): Offset to start the list.
        limit (int): Limit of studies to be listed.
        session (DBSessionDep): Database session.
        ctx (Context): Context object.

    Returns:
        list[StudyPublic]: List of studies.
    """
    user_id = ctx.get_user_id()
    logger = ctx.get_logger()
    
    if organization_id:
        ctx.without_global_filtering()

    try:
        studies = study_crud.get_studies(
            session,
            user_id=user_id,
            offset=offset,
            limit=limit,
            organization_id=organization_id,
        )
        return studies
    except Exception as e:
        logger.exception(event=e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{study_id}", response_model=StudyPublic)
async def get_study_by_id(
    study_id: str, 
    session: DBSessionDep, 
    ctx: Context = Depends(get_context)
) -> Study:
    """
    Get study by ID.

    Args:
        study_id (str): Study ID.
        session (DBSessionDep): Database session.
        ctx (Context): Context object.

    Returns:
        Study: Study.

    Raises:
        HTTPException: If the study is not found.
    """
    user_id = ctx.get_user_id()
    study = None

    try:
        study = study_crud.get_study_by_id(session, study_id, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not study:
        raise HTTPException(
            status_code=404,
            detail=f"Study with ID {study_id} not found.",
        )

    study_schema = Study.model_validate(study)
    ctx.with_study(study_schema)
    return study

@router.put(
    "/{study_id}",
    response_model=StudyPublic,
    dependencies=[
        Depends(validate_user_header),
        Depends(validate_update_study_request),
    ],
)
async def update_study(
    study_id: str,
    new_study: UpdateStudyRequest,
    session: DBSessionDep,
    ctx: Context = Depends(get_context),
) -> StudyPublic:
    """
    Update a study by ID.

    Args:
        study_id (str): Study ID.
        new_study (UpdateStudyRequest): New study data.
        session (DBSessionDep): Database session.
        ctx (Context): Context object.

    Returns:
        StudyPublic: Updated study.

    Raises:
        HTTPException: If the study is not found.
    """
    user_id = ctx.get_user_id()
    ctx.with_user(session)
    study = validate_study_exists(session, study_id, user_id)

    try:
        study = study_crud.update_study(
            session, study, new_study, user_id
        )
        study_schema = Study.model_validate(study)
        ctx.with_study(study_schema)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return study

@router.delete("/{study_id}", response_model=DeleteStudy)
async def delete_study(
    study_id: str,
    session: DBSessionDep,
    ctx: Context = Depends(get_context),
) -> DeleteStudy:
    """
    Delete a study by ID.

    Args:
        study_id (str): Study ID.
        session (DBSessionDep): Database session.
        ctx (Context): Context object.

    Returns:
        DeleteStudy: Empty response.

    Raises:
        HTTPException: If the study is not found.
    """
    user_id = ctx.get_user_id()
    study = validate_study_exists(session, study_id, user_id)
    study_schema = Study.model_validate(study)
    ctx.with_study(study_schema)

    deleted = study_crud.delete_study(session, study_id, user_id)
    if not deleted:
        raise HTTPException(status_code=401, detail="Could not delete Study.")

    return DeleteStudy()
