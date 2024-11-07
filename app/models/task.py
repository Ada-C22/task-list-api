from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)
    is_complete: Mapped[bool] = mapped_column(default=False)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_dict = dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.is_complete
        )
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data.get("title"),
            description=task_data.get("description"),
            is_complete=task_data.get("is_complete"),
            goal_id=task_data.get("goal_id")
        )
