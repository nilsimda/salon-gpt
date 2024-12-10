from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, Field


class Citation(BaseModel):
    """
    Represents a single quote with a confidence score.
    """

    text: str = Field(..., description="Zitat aus dem Interview")
    confidence_score: Annotated[
        float,
        Field(
            gt=0,
            lt=1,
            description="Wie sicher bist du dir mit deiner Antwort auf einer Skala von 0.0-1.0",
        ),
    ]


class CitationList(BaseModel):
    """
    Represents a list of quotes.
    """

    zitate: Annotated[list[Citation], Len(min_length=1, max_length=10)]
