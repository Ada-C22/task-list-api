from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from datetime import datetime 
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")


    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.completed_at is not None 
        if self.goal:
            task_as_dict["goal_id"] = self.goal.id
        else:
            None

        return task_as_dict

    @classmethod
    def from_dict(cls, task_data):
        goal_id = task_data.get("goal_id")
        new_task = cls(title=task_data["title"], 
                        description=task_data["description"],
                        goal_id=goal_id
                        )
        
        return new_task