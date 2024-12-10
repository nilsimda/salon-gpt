import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from backend.schemas.message import Message


class Conversation(BaseModel):
    id: str
    user_id: str
    agent_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    title: str
    messages: List[Message]
    description: Optional[str]
    is_pinned: bool

    class Config:
        from_attributes = True


class ConversationWithoutMessages(Conversation):
    messages: List[Message] = Field(exclude=True)


class UpdateConversationRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class ToggleConversationPinRequest(BaseModel):
    is_pinned: bool


class DeleteConversationResponse(BaseModel):
    pass


class GenerateTitleResponse(BaseModel):
    title: str
    error: Optional[str] = None
