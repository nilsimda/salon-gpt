from sqlalchemy.orm import Session

from backend.database_models.interview import Interview
from backend.services.transaction import validate_transaction


@validate_transaction
def get_interviews_by_ids(db: Session, interview_ids: list[str]) -> list[Interview]:
    """
    Get interviews by IDs.

    Args:
        db (Session): Database session.
        interview_ids (list[str]): File IDs.

    Returns:
        list[Interview]: List of files with the given IDs.
    """
    return db.query(Interview).filter(Interview.id.in_(interview_ids)).all()
