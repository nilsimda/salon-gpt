from uuid import uuid4

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database_models.base import Base


class Interview(Base):
    __tablename__ = "interviews"

    interview_id: Mapped[str] = mapped_column(
        String, default=lambda: str(uuid4()), unique=True, primary_key=True
    )
    text: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    interview_class: Mapped[str] = mapped_column(String, nullable=False)
    fields: Mapped[dict] = mapped_column(JSON, nullable=True)
    study_id: Mapped[str] = mapped_column(ForeignKey("studies.id"), nullable=False)
    study = relationship("Study", back_populates="interviews")
