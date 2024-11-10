from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.database_models.base import Base


class Study(Base):
    __tablename__ = "studies"

    name: Mapped[str] = mapped_column(Text, nullable=False)
    individual_interview_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    group_interview_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
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
