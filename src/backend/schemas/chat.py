from enum import StrEnum
from typing import Any, ClassVar, Dict, List, Union
from uuid import uuid4

from pydantic import BaseModel, Field

from backend.chat.enums import StreamEvent
from backend.schemas.citation import Citation
from backend.schemas.interview import Interview


class ChatRole(StrEnum):
    """One of CHATBOT|USER|SYSTEM to identify who the message is coming from."""

    CHATBOT = "CHATBOT"
    USER = "USER"
    SYSTEM = "SYSTEM"

class ChatMessage(BaseModel):
    """A list of previous messages between the user and the model, meant to give the model conversational context for responding to the user's message."""

    role: ChatRole = Field(
        title="One of CHATBOT|USER|SYSTEM to identify who the message is coming from.",
    )
    message: str | None = Field(
        title="Contents of the chat message.",
        default=None,
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "message": self.message,
        }


# TODO: fix titles of these types
class ChatResponse(BaseModel):
    event_type: ClassVar[StreamEvent] = Field()


class StreamStart(ChatResponse):
    """Stream start event."""

    event_type: ClassVar[StreamEvent] = StreamEvent.STREAM_START
    generation_id: str | None = Field(default=None)
    conversation_id: str | None = Field(default=None)


class StreamTextGeneration(ChatResponse):
    """Stream text generation event."""

    event_type: ClassVar[StreamEvent] = StreamEvent.TEXT_GENERATION

    text: str = Field(
        title="Contents of the chat message.",
    )

class StreamSearchResults(ChatResponse):
    event_type: ClassVar[StreamEvent] = StreamEvent.SEARCH_RESULTS

    search_results: List[Dict[str, Any]] = Field(
        title="Search results used to generate grounded response with citations.",
        default=[],
    )
    interview: Interview = Field(
        title="The interview in which was searched",
        default=None,
    )


class StreamEnd(ChatResponse):
    message_id: str | None = Field(default=None)
    response_id: str | None = Field(default=None)
    event_type: ClassVar[StreamEvent] = StreamEvent.STREAM_END
    generation_id: str | None = Field(default=None)
    conversation_id: str | None = Field(default=None)
    text: str = Field(
        title="Contents of the chat message.",
    )
    citations: List[Citation] = Field(
        title="Citations for the chat message.", default=[]
    )
    documents: List[Interview] = Field(
        title="Interviews used to generate grounded response with citations.",
        default=[],
    )
    search_results: List[Dict[str, Any]] = Field(
        title="Search results used to generate grounded response with citations.",
        default=[],
    )
    finish_reason: str | None = (Field(default=None),)
    chat_history: List[ChatMessage] | None = Field(
        default=None,
        title="A list of entries used to construct the conversation. If provided, these messages will be used to build the prompt and the conversation_id will be ignored so no data will be stored to maintain state.",
    )
    error: str | None = Field(
        title="Error message if the response is an error.",
        default=None,
    )


class NonStreamedChatResponse(ChatResponse):
    response_id: str | None = Field(
        title="Unique identifier for the response.",
    )
    generation_id: str | None = Field(
        title="Unique identifier for the generation.",
    )
    chat_history: List[ChatMessage] | None = Field(
        title="A list of previous messages between the user and the model, meant to give the model conversational context for responding to the user's message.",
    )
    finish_reason: str = Field(
        title="Reason the chat stream ended.",
    )
    text: str = Field(
        title="Contents of the chat message.",
    )
    citations: List[Citation] | None = Field(
        title="Citations for the chat message.",
        default=[],
    )
    documents: List[Interview] | None = Field(
        title="Interviews used to generate grounded response with citations.",
        default=[],
    )
    search_results: List[Dict[str, Any]] | None = Field(
        title="Search results used to generate grounded response with citations.",
        default=[],
    )
    conversation_id: str | None = Field(
        title="To store a conversation then create a conversation id and use it for every related request.",
    )
    error: str | None = Field(
        title="Error message if the response is an error.",
        default=None,
    )

StreamEventType = Union[
    StreamStart,
    StreamTextGeneration,
    StreamEnd,
    NonStreamedChatResponse,
]

class ChatResponseEvent(BaseModel):
    event: StreamEvent = Field(
        title="type of stream event",
    )

    data: StreamEventType = Field(
        title="Data returned from chat response of a given event type",
    )

class BaseChatRequest(BaseModel):
    user_id: str = Field(
         title="A user id to store to store the conversation under.", exclude=True
    )

    description: str = Field(
        title="The description of the synthetic user.",
    )

    message: str = Field(
        title="The message to send to the chatbot.",
    )
    chat_history: List[ChatMessage] | None = Field(
        default=None,
        title="A list of entries used to construct the conversation. If provided, these messages will be used to build the prompt and the conversation_id will be ignored so no data will be stored to maintain state.",
    )
    conversation_id: str = Field(
        default_factory=lambda: str(uuid4()),
        title="To store a conversation then create a conversation id and use it for every related request",
    )
