from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import Optional
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]

    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))

    goal: Mapped[Optional["Goal"]] = relationship("Goal", back_populates="tasks")
    
    def to_dict(self):
        task_as_dict ={
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at),
        }

        if self.goal:
            task_as_dict ={
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at),
            "goal_id": self.goal_id # just for wave 6
        }
            
        return task_as_dict