from typing import List, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.database_models.base import Base


class Study(Base):
    __tablename__ = "studies"

    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    individual_interview_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ti_files: Mapped[List[str]] = mapped_column(Text, nullable=True)
    gd_files: Mapped[List[str]] = mapped_column(Text, nullable=True)
    memo_files: Mapped[List[str]] = mapped_column(Text, nullable=True)
    metadata_file: Mapped[str] = mapped_column(Text, nullable=True)
    is_being_added: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Foreign key relationships
    organization_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey(
            "organizations.id", name="studies_organization_id_fkey", ondelete="CASCADE"
        )
    )

    # Ensure study names are unique
    __table_args__ = (
        UniqueConstraint("name", name="_study_name_uc"),
    )
