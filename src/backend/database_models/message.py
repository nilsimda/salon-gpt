from enum import StrEnum
from typing import List

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKeyConstraint,
    Index,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database_models.base import Base


class MessageAgent(StrEnum):
    USER = "user"
    CHATBOT = "assistant"


class Message(Base):
    """
    Default Message model for conversation text.
    """

    __tablename__ = "messages"

    text: Mapped[str]

    user_id: Mapped[str] = mapped_column(String, nullable=True)
    conversation_id: Mapped[str] = mapped_column(String, nullable=True)
    position: Mapped[int]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    generation_id: Mapped[str] = mapped_column(String, nullable=True)

    agent: Mapped[MessageAgent] = mapped_column(
        Enum(MessageAgent, native_enum=False),
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["conversation_id", "user_id"],
            ["conversations.id", "conversations.user_id"],
            name="message_conversation_id_user_id_fkey",
            ondelete="CASCADE",
        ),
        Index("message_conversation_id_user_id", conversation_id, user_id),
        Index("message_conversation_id", conversation_id),
        Index("message_is_active", is_active),
        Index("message_user_id", user_id),
    )
