from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import String, Boolean, ForeignKey
from typing import Optional


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[str | None] = mapped_column(String, nullable=True)
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self, include_goal_id=False):
        response = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None,
        }
        if include_goal_id and self.goal_id is not None:
            response["goal_id"] = self.goal_id
        return response

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data['title'],
            description=task_data['description'],
            goal_id=task_data.get("goal_id", None)
        )
