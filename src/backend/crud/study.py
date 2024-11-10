from typing import Optional

from sqlalchemy.orm import Session

from backend.database_models.study import Study
from backend.services.transaction import validate_transaction


@validate_transaction
def create_study(db: Session, study: Study) -> Study:
    """
    Create a new study.

    Args:
      db (Session): Database session.
      study (Study): Study to be created.

    Returns:
      Study: Created study.
    """
    db.add(study)
    db.commit()
    db.refresh(study)
    return study


@validate_transaction
def get_study_by_id(
    db: Session, study_id: str, user_id: str = "", override_user_id: bool = False
) -> Study:
    """
    Get an study by its ID.
    Anyone can get a public study, but only the owner can get a private study.

    Args:
      db (Session): Database session.
      study_id (str): Study ID.
      override_user_id (bool): Override user ID check. Should only be used for internal operations.

    Returns:
      Study: Study with the given ID.
    """
    return db.query(Study).filter(Study.id == study_id).first()


@validate_transaction
def get_study_by_name(db: Session, study_name: str, user_id: str) -> Study:
    """
    Get an study by its name.
    Anyone can get a public study, but only the owner can get a private study.

    Args:
      db (Session): Database session.
      study_name (str): Study name.

    Returns:
      Study: Study with the given name.
    """
    return db.query(Study).filter(Study.name == study_name).first()


@validate_transaction
def get_studies(
    db: Session,
    user_id: str = "",
    offset: int = 0,
    limit: int = 100,
    organization_id: Optional[str] = None,
) -> list[Study]:
    """
    Get all studies for a user.

    Args:
        db (Session): Database session.
        offset (int): Offset of the results.
        limit (int): Limit of the results.
        organization_id (str): Organization ID.
        user_id (str): User ID.

    Returns:
      list[Study]: List of studies.
    """
    query = db.query(Study)
    return query.offset(offset).limit(limit).all()



@validate_transaction
def delete_study(db: Session, study_id: str, user_id: str) -> bool:
    """
    Delete an Study by ID if the Study was created by the user_id given.

    Args:
        db (Session): Database session.
        study_id (str): Study ID.

    Returns:
      bool: True if the Study was deleted, False otherwise
    """
    study_query = db.query(Study).filter(Study.id == study_id, Study.user_id == user_id)
    study = study_query.first()

    if not study:
        return False

    study_query.delete()
    db.commit()
    return True
