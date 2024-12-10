from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from backend.config.routers import RouterName
from backend.crud import study as study_crud
from backend.database_models.database import DBSessionDep
from backend.database_models.study import Study as StudyModel
from backend.schemas.interview import Interview
from backend.schemas.study import (
    CreateStudyRequest,
    DeleteStudy,
    Study,
    UpdateStudyRequest,
)
from backend.services.request_validators import (
    validate_create_study_request,
    validate_update_study_request,
    validate_user_header,
)
from backend.services.study import (
    validate_study_exists,
)

router = APIRouter(
    prefix="/v1/studies",
)
router.name = RouterName.STUDY  # type: ignore


@router.post(
    "",
    response_model=Study,
    dependencies=[
        Depends(validate_user_header),
        Depends(validate_create_study_request),
    ],
)
async def create_study(
    session: DBSessionDep,
    study: CreateStudyRequest,
) -> Study:
    """
    Create a study.

    Args:
        session (DBSessionDep): Database session.
        study (CreateStudyRequest): Study data.
          (Context): Context object.
    Returns:
        Study: Created study with no user ID or organization ID.
    Raises:
        HTTPException: If the study creation fails.
    """
    study_data = StudyModel(
        name=study.name,
        description=study.description,
        group_interview_count=study.group_interview_count,
        is_being_added=False,
    )

    try:
        created_study = study_crud.create_study(session, study_data)
        return created_study
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=list[Study])
async def list_studies(
    *,
    offset: int = 0,
    limit: int = 100,
    session: DBSessionDep,
    organization_id: Optional[str] = None,
) -> list[Study]:
    """
    List all studies.

    Args:
        offset (int): Offset to start the list.
        limit (int): Limit of studies to be listed.
        session (DBSessionDep): Database session.
          (Context): Context object.

    Returns:
        list[Study]: List of studies.
    """
    try:
        studies = study_crud.get_studies(
            session,
            offset=offset,
            limit=limit,
            organization_id=organization_id,
        )
        return studies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{study_id}", response_model=Study)
async def get_study_by_id(study_id: str, session: DBSessionDep) -> Study:
    """
    Get study by ID.

    Args:
        study_id (str): Study ID.
        session (DBSessionDep): Database session.
          (Context): Context object.

    Returns:
        Study: Study.

    Raises:
        HTTPException: If the study is not found.
    """
    study = None

    try:
        study = study_crud.get_study_by_id(session, study_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not study:
        raise HTTPException(
            status_code=404,
            detail=f"Study with ID {study_id} not found.",
        )

    return study


@router.put(
    "/{study_id}",
    response_model=Study,
    dependencies=[
        Depends(validate_user_header),
        Depends(validate_update_study_request),
    ],
)
async def update_study(
    study_id: str,
    new_study: UpdateStudyRequest,
    session: DBSessionDep,
) -> Study:
    """
    Update a study by ID.

    Args:
        study_id (str): Study ID.
        new_study (UpdateStudyRequest): New study data.
        session (DBSessionDep): Database session.
          (Context): Context object.

    Returns:
        Study: Updated study.

    Raises:
        HTTPException: If the study is not found.
    """
    study = validate_study_exists(session, study_id)

    try:
        study = study_crud.update_study(session, study, new_study)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return study


@router.delete("/{study_id}", response_model=DeleteStudy)
async def delete_study(
    study_id: str,
    session: DBSessionDep,
) -> DeleteStudy:
    """
    Delete a study by ID.

    Args:
        study_id (str): Study ID.
        session (DBSessionDep): Database session.
          (Context): Context object.

    Returns:
        DeleteStudy: Empty response.

    Raises:
        HTTPException: If the study is not found.
    """
    study = validate_study_exists(session, study_id)
    deleted = study_crud.delete_study(session, study_id)
    if not deleted:
        raise HTTPException(status_code=401, detail="Could not delete Study.")

    return DeleteStudy()


@router.get("/{study_id}/interviews", response_model=list[Interview])
async def list_files(study_id: str, session: DBSessionDep) -> list[Interview]:
    """
    List all interviews from a study. Important - no pagination support yet.

    Args:
        study_id (str): Study ID.
        session (DBSessionDep): Database session.
          (Context): Context object.

    Returns:
        list[Interview]: List of interviews from the study.

    Raises:
        HTTPException: If the study with the given ID is not found.
    """
    _ = validate_study_exists(session, study_id)

    return study_crud.get_interviews_by_study(session, study_id)
