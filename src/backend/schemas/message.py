import datetime
from typing import List, Optional, Union

from pydantic import BaseModel

from backend.database_models.message import MessageAgent
from backend.schemas.citation import Citation
from backend.schemas.file import ConversationFilePublic
from backend.schemas.interview import Interview


class MessageBase(BaseModel):
    text: str


class Message(MessageBase):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    generation_id: Union[str, None]

    position: int
    is_active: bool

    documents: List[Interview]
    citations: List[Citation]
    files: List[ConversationFilePublic]

    agent: MessageAgent

    class Config:
        from_attributes = True


class UpdateMessage(BaseModel):
    text: Optional[str] = None
    title: Optional[str] = None

    class Config:
        from_attributes = True
