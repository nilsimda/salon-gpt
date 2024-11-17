from typing import List
from uuid import uuid4

from sqlalchemy import Boolean, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database_models.base import Base


class Study(Base):
    __tablename__ = "studies"

    id: Mapped[str] = mapped_column(String, default=lambda: str(uuid4()), unique=True, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    ti_files: Mapped[List[str]] = mapped_column(Text, nullable=True)
    gd_files: Mapped[List[str]] = mapped_column(Text, nullable=True)
    memo_files: Mapped[List[str]] = mapped_column(Text, nullable=True)
    metadata_file: Mapped[str] = mapped_column(Text, nullable=True)
    is_being_added: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    interviews = relationship("Interview", back_populates="study")

    # Ensure study names are unique
    __table_args__ = (
        UniqueConstraint("name", name="_study_name_uc"),
    )
