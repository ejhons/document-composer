from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class ProjectResponse(BaseModel):
    id: str
    name: str