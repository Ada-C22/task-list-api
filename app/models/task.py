from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional
from datetime import datetime


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    # completed_at:Mapped[datetime] = mapped_column(default=None, nullable=True)
    completed_at: Mapped[Optional[datetime]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            goal_id=task_data.get("goal_id"),
        )

    @classmethod
    def attr_list(cls):
        return ["title", "description"]

    def to_dict(self):
        completed = False
        if self.completed_at:
            completed = True

        response = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": completed,
        }
        
        if self.goal_id:
            response["goal_id"] = self.goal_id

        return response