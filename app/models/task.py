from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey('goal.id'), nullable=True)
    goal: Mapped["Goal"] = relationship("Goal", back_populates="tasks")

    def task_dict(self):
        task_data = {
            "id": self.id, 
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }

        if self.goal_id is not None:
            task_data["goal_id"] = self.goal_id
        return task_data
        