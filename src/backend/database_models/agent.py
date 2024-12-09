from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database_models.base import Base


class Agent(Base):
    __tablename__ = "agents"

    name: Mapped[str] = mapped_column(
        Text, nullable=False, unique=True, primary_key=True
    )
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    model: Mapped[str] = mapped_column(Text, nullable=False)
