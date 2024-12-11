from typing import Annotated

from pydantic import BaseModel, Field


class Citation(BaseModel):
    erklaerung: str = Field(..., description="Eine Erklärung, warum das Zitat relevant ist.")
    text: str = Field(..., description="Der eigentliche Text des Zitats.")
    bewertung: Annotated[
        float,
        Field(
            ...,
            description="Die Zuversichtlichkeit des Modells, dass das Zitat korrekt ist.",
        ),
    ]


class CitationList(BaseModel):
    zitate: list[Citation] = Field(
        ..., description="Eine Liste von Zitaten, die in einem Text gefunden wurden."
    )
