from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy import DateTime, Boolean
from typing import Optional
from ..models.goal import Goal


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["completed_at"] = self.completed_at
        task_as_dict["is_complete"] = self.is_complete

        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id

        return task_as_dict

    @classmethod
    def from_dict(cls, data):
        goal_id = data.get("goal_id")
        if not goal_id:
            return cls(
                title=data["title"],
                description=data["description"],
                completed_at=None,
                is_complete=False,
            )
        else:
            return cls(
                title=data["title"],
                description=data["description"],
                completed_at=None,
                is_complete=False,
                goal_id=data.get("goal_id"),
            )

    def create_response(self):
        response = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete,
        }
        if self.goal_id:
            response["goal_id"] = self.goal_id
        return response
