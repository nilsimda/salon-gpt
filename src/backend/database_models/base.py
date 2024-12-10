from uuid import uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Query, mapped_column


class CustomFilterQuery(Query):
    """
    Custom query class that filters by field if the entity has field
    and the filter value is set.
    """

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)


class MinimalBase(DeclarativeBase):
    pass


class Base(DeclarativeBase):
    id = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    created_at = mapped_column(
        DateTime,
        default=func.now(),
    )

    updated_at = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
