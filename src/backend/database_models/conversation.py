from typing import List
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Index,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database_models.base import Base
from backend.database_models.message import Message


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String, default=lambda: str(uuid4()), unique=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    agent_id: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String, default="Neue Konversation")
    description: Mapped[str] = mapped_column(String, nullable=True, default=None)
    text_messages: Mapped[List["Message"]] = relationship()
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)

    @property
    def messages(self):
        return sorted(self.text_messages, key=lambda x: x.created_at)

    __table_args__ = (
        UniqueConstraint("id", "user_id", name="conversation_id_user_id"),
        PrimaryKeyConstraint("id", "user_id", name="conversation_pkey"),
        Index("conversation_user_agent_index", "user_id", "agent_id"),
        Index("conversation_user_id_index", "id", "user_id", unique=True),
    )
