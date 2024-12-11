from enum import Enum, StrEnum
from typing import Any, ClassVar, Dict, List, Union
from uuid import uuid4

from pydantic import BaseModel, Field

from backend.schemas.citation import CitationList
from backend.schemas.interview import Interview


class StreamEvent(str, Enum):
    """
    Stream Events returned by Cohere's chat stream response.
    """

    STREAM_START = "stream-start"
    SEARCH_RESULTS = "search-results"
    TEXT_GENERATION = "text-generation"
    STREAM_END = "stream-end"


class ChatRole(StrEnum):
    """One of model|user|system to identify who the message is coming from."""

    MODEL = "model"
    USER = "user"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """A list of previous messages between the user and the model, meant to give the model conversational context for responding to the user's message."""

    role: ChatRole = Field(
        title="One of model|user|system to identify who the message is coming from.",
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

    search_results: CitationList = Field(
        title="Search results found in the interview",
    )
    interview_id: str = Field(
        title="The id of the interview in which was searched",
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
    search_results: dict[str, CitationList] | None = Field(title="Search results found in the interviews", default=None)
    finish_reason: str | None = Field(title="The finish reason", default=None)
    chat_history: List[ChatMessage] | None = Field(
        default=None,
        title="A list of entries used to construct the conversation. If provided, these messages will be used to build the prompt and the conversation_id will be ignored so no data will be stored to maintain state.",
    )
    error: str | None = Field(
        title="Error message if the response is an error.",
        default=None,
    )


StreamEventType = Union[
    StreamStart,
    StreamTextGeneration,
    StreamSearchResults,
    StreamEnd,
]


class ChatResponseEvent(BaseModel):
    event: StreamEvent = Field(
        title="type of stream event",
    )

    data: StreamEventType = Field(
        title="Data returned from chat response of a given event type",
    )


class SalonChatRequest(BaseModel):
    user_id: str = Field(
        title="A user id to store to store the conversation under.", exclude=True
    )

    agent_id: str = Field(
        title="The agent_id to use for the chat request. This allows us to construct the correct system prompt.",
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
    # these options are only used for the search task
    study_id: str | None = Field(title="The study_id to use for the chat request.", default=None)
    interview_ids: list[str] | None = Field(title="The interview_ids that should be searched.", default=None)
    interviews: list[Interview] | None = Field(title="The interviews that should be searched.", default=None)

    # this option is only used for the syntehtic user task
    description: str | None = Field(title="Description of the user to simulate.", default=None)
