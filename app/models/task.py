from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped["Goal"] = relationship("Goal", back_populates="tasks")
    


    def to_dict(self):
        task_as_dict = {
            "id": self.id, 
            "title": self.title, 
            "description": self.description, 
            "is_complete": check_for_completion(self)
        }
        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id
        
        return task_as_dict


    @classmethod
    def from_dict(cls, task_data):
        goal_id = task_data.get("goal_id")
        
        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
            goal_id = goal_id
        )
        return new_task
    
def check_for_completion(self):
    if self.completed_at is not None:
        return True
    else :
        return False