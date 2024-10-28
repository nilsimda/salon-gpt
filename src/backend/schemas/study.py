from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StudyBase(BaseModel):
    user_id: str
    organization_id: Optional[str] = None


class Study(StudyBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    name: str
    individual_interview_count: int = 0
    group_interview_count: int = 0

    class Config:
        from_attributes = True


class StudyPublic(Study):
    organization_id: Optional[str] = Field(exclude=True)


class CreateStudyRequest(BaseModel):
    name: str
    individual_interview_count: Optional[int] = 0
    group_interview_count: Optional[int] = 0
    organization_id: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateStudyRequest(BaseModel):
    name: Optional[str] = None
    individual_interview_count: Optional[int] = None
    group_interview_count: Optional[int] = None
    organization_id: Optional[str] = None

    class Config:
        from_attributes = True


class DeleteStudy(BaseModel):
    pass


class ListStudiesResponse(BaseModel):
    studies: list[Study]