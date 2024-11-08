from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from datetime import date
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[date] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
        )

    def check_completion(self):
        if not self.completed_at:
            return False
        return True
    
    def to_dict(self):
        task_dict = dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.check_completion()
            )
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict


