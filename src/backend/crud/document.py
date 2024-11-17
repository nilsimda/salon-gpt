from sqlalchemy.orm import Session

from backend.database_models.document import Interview
from backend.services.transaction import validate_transaction


@validate_transaction
def create_document(db: Session, document: Interview) -> Interview:
    """
    Create a new document.

    Args:
        db (Session): Database session.
        document (Interview): Interview data to be created.

    Returns:
        Interview: Created document.
    """
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@validate_transaction
def get_document(db: Session, document_id: str) -> Interview:
    """
    Get a document by ID.

    Args:
        db (Session): Database session.
        document_id (str): Interview ID.

    Returns:
        Interview: Interview with the given ID.
    """
    return db.query(Interview).filter(Interview.id == document_id).first()


@validate_transaction
def get_documents(db: Session, offset: int = 0, limit: int = 100) -> list[Interview]:
    """
    List all documents.

    Args:
        db (Session): Database session.
        offset (int): Offset to start the list.
        limit (int): Limit of documents to be listed.

    Returns:
        list[Interview]: List of documents.
    """
    return db.query(Interview).offset(offset).limit(limit).all()


def delete_document(db: Session, document_id: str) -> None:
    """
    Delete a document by ID.

    Args:
        db (Session): Database session.
        document_id (str): Interview ID.
    """
    document = db.query(Interview).filter(Interview.id == document_id)
    document.delete()
    db.commit()
