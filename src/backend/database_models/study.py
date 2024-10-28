from typing import Optional

from sqlalchemy import ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database_models.base import Base


class Study(Base):
    __tablename__ = "studies"

    name: Mapped[str] = mapped_column(Text, nullable=False)
    individual_interview_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    group_interview_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Foreign key relationships (assuming you want to associate studies with users/organizations)
    user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("users.id", name="studies_user_id_fkey", ondelete="CASCADE")
    )
    organization_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey(
            "organizations.id", name="studies_organization_id_fkey", ondelete="CASCADE"
        )
    )

    # Relationships
    user = relationship("User", back_populates="studies")

    # Ensure study names are unique per user
    __table_args__ = (
        UniqueConstraint("name", "user_id", name="_study_name_user_uc"),
    )
