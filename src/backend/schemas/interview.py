from typing import Optional

from pydantic import BaseModel


class Interview(BaseModel):
    text: str
    interview_id: str

    title: str
    interview_class: str
    fields: Optional[dict] = None

    class Config:
        from_attributes = True
