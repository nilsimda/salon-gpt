from enum import StrEnum
from typing import Union

from pydantic import BaseModel


class InterviewType(StrEnum):
    GD = "GD"
    TI = "TI"
    Memo = "Memo"

class InterviewBase(BaseModel):
    pass


class Interview(BaseModel):
    text: str
    id: str

    title: Union[str, None]
    type: InterviewType
    fields: Union[dict, None]

    class Config:
        from_attributes = True
