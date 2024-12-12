from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Study(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime

    name: str
    is_transcribed: bool = False
    description: Optional[str] = None

    class Config:
        from_attributes = True


class CreateStudyRequest(BaseModel):
    name: str
    description: Optional[str] = None
    is_transcribed: Optional[bool] = False

    class Config:
        from_attributes = True


class UpdateStudyRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_transcribed: Optional[bool] = False

    class Config:
        from_attributes = True


class DeleteStudy(BaseModel):
    pass


class ListStudiesResponse(BaseModel):
    studies: list[Study]
