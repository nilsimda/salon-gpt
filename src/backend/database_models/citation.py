from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.database_models.base import Base


class Citation(Base):
    __tablename__ = "citations"

    text: Mapped[str]
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    start: Mapped[int]
    end: Mapped[int]

    message_id: Mapped[str] = mapped_column(
        ForeignKey("messages.id", ondelete="CASCADE")
    )
