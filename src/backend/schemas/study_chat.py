from pydantic import Field

from backend.schemas.cohere_chat import BaseChatRequest


class StudyChatRequest(BaseChatRequest):
    study_id: str = Field(
        title = "The study ID of the study for which to search in"
    )

    temperature: float | None = Field(
        default=None,
        title="A non-negative float that tunes the degree of randomness in generation. Lower temperatures mean less random generations, and higher temperatures mean more random generations.",
        ge=0,
    )

    model: str | None = Field(
        default="llama3.2",
        title="The model to use for generating the search query and potentially the response.",
    )

    search_only: bool | None = Field(
        default=True,
        title="When set to true just do a semantic search no generation."
    )


