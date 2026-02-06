from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(SQLModel):
    description: str = Field(min_length=1, max_length=500)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    __tablename__ = "task"
    __table_args__ = {"extend_existing": True}  # <- This prevents duplicate table errors

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    def __str__(self):
        status = "completed" if self.completed else "pending"
        return f"{self.description} [{status}]"

