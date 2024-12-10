import datetime
from typing import Optional, Union

from pydantic import BaseModel

from backend.database_models.message import MessageAgent


class MessageBase(BaseModel):
    text: str


class Message(MessageBase):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    generation_id: Union[str, None]

    position: int
    is_active: bool

    agent: MessageAgent

    class Config:
        from_attributes = True


class UpdateMessage(BaseModel):
    text: Optional[str] = None
    title: Optional[str] = None

    class Config:
        from_attributes = True
