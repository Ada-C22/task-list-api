from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at:Mapped[datetime] = mapped_column(default=None, nullable=True)
    goal_id: Mapped[Optional[int]]=mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):

        task_dict = dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete= True if self.completed_at else False
        )

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    @classmethod
    def from_dict(cls, task_data):
        if "completed_at" in task_data:
            return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data["completed_at"]
            )

        return cls(
            title=task_data["title"],
            description=task_data["description"],
        )