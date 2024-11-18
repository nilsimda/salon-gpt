from fastapi import HTTPException

from backend.crud import study as study_crud
from backend.database_models.database import DBSessionDep
from backend.database_models.study import Study


def validate_study_exists(session: DBSessionDep, study_id: str, user_id: str) -> Study:
    study = study_crud.get_study_by_id(session, study_id)

    if not study:
        raise HTTPException(
            status_code=404,
            detail=f"Study with ID {study_id} not found.",
        )

    return study

def raise_db_error(e: Exception, type: str, name: str):
    if "psycopg2.errors.UniqueViolation" in str(e):
        raise HTTPException(
            status_code=400,
            detail=f"{type} {name} already exists for given user.",
        )

    raise HTTPException(status_code=500, detail=str(e))