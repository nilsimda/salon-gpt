from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Study(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime

    name: str
    ti_files: Optional[list[str]] = None
    gd_files: Optional[list[str]] = None
    memo_files: Optional[list[str]] = None
    metadata_file: Optional[str] = None
    is_being_added: bool = True
    organization_id: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class CreateStudyRequest(BaseModel):
    name: str
    individual_interview_count: Optional[int] = 0
    group_interview_count: Optional[int] = 0
    organization_id: Optional[str] = None
    description: Optional[str] = None
    is_being_added: Optional[bool] = True

    class Config:
        from_attributes = True


class UpdateStudyRequest(BaseModel):
    name: Optional[str] = None
    individual_interview_count: Optional[int] = None
    group_interview_count: Optional[int] = None
    organization_id: Optional[str] = None
    description: Optional[str] = None
    is_being_added: Optional[bool] = False

    class Config:
        from_attributes = True


class DeleteStudy(BaseModel):
    pass


class ListStudiesResponse(BaseModel):
    studies: list[Study]
