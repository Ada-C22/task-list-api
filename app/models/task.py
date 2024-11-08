from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from sqlalchemy import ForeignKey
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship("Goal", back_populates="tasks")


    def to_dict(self, include_goal=False, include_goal_id=False):
        task_dict = dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.completed_at is not None 
        )
        if include_goal_id:
            task_dict["goal_id"] = self.goal_id

        if include_goal and self.goal:
            task_dict['goal'] = self.goal.title 

        
        return task_dict
    
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = task_data.get("completed_at"),
            goal_id=task_data.get("goal_id", None)
        )
