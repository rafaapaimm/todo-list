from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""
    priority: str = Field(default="medium")

    @property
    def normalized_priority(self) -> str:
        return self.priority.lower()


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    completed: bool
    created_at: str
    updated_at: str
