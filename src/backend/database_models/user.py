from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.database_models.base import Base


class User(Base):
    __tablename__ = "users"

    user_name: Mapped[Optional[str]] = mapped_column()
    fullname: Mapped[str] = mapped_column()
    external_id: Mapped[Optional[str]] = mapped_column()
    active: Mapped[Optional[bool]] = mapped_column()

    email: Mapped[Optional[str]] = mapped_column()
    hashed_password: Mapped[Optional[bytes]] = mapped_column()

    __table_args__ = (
        UniqueConstraint("email", name="unique_user_email"),
        UniqueConstraint("user_name", name="unique_user_name"),
    )
