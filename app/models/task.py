from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from datetime import datetime
from typing import Optional


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship("Goal", back_populates="tasks")

    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": task.is_complete()})
        }
        if self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id
        return task_dict

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            goal_id=task_data.get("goal_id"),
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at", None),
        )
