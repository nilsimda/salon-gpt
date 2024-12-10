from typing import Annotated
from pydantic import BaseModel, Field


class Citation(BaseModel):
    text: str = Field(..., description="Der eigentliche Text des Zitats.")
    confidence_score: Annotated[
        float,
        Field(
            ...,
            description="Die Zuversichtlichkeit des Modells, dass das Zitat korrekt ist.",
            gt=0,
            lt=1,
        ),
    ]


class CitationList(BaseModel):
    zitate: list[Citation] = Field(
        ..., description="Eine Liste von Zitaten, die in einem Text gefunden wurden."
    )
