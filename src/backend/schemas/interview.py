from typing import Optional

from pydantic import BaseModel


class Interview(BaseModel):
    text: str
    id: str

    title: str
    interview_type: str
    fields: Optional[dict] = None
    study_id: str

    class Config:
        from_attributes = True


class InterviewChunk(BaseModel):
    interview_id: str
    original_text: str
    start_pos: int
    end_pos: int
    bm25_tokens: list[str]
