from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal


class UserCreate(BaseModel):
    name: str
    email: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str
    owner_id: int


class ProjectOut(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: Optional[str] = None
    project_id: int

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Title khali nahi ho sakta")
        return value.strip()


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    due_date: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("Title khali nahi ho sakta")
        return value.strip() if value else value


class TaskOut(BaseModel):
    id: int
    title: str
    priority: str
    due_date: Optional[str]
    project_id: int

    class Config:
        from_attributes = True


class ProjectStats(BaseModel):
    project_id: int
    project_name: str
    total_tasks: int