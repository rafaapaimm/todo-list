from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    id: int | None = None
    title: str = ""
    description: str = ""
    priority: str = "medium"
    completed: bool = False
    created_at: str | None = None
    updated_at: str | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at or datetime.utcnow().isoformat(),
            "updated_at": self.updated_at or datetime.utcnow().isoformat(),
        }
