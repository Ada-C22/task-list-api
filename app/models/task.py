from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import DateTime, ForeignKey
from datetime import datetime
from typing import Optional

# from app.models.goal import Goal


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title : Mapped[str] = mapped_column() 
    description: Mapped[str] = mapped_column()
    completed_at : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    goal_id : Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal : Mapped[Optional["Goal"]] = relationship(back_populates="tasks") # its an attribute not a column

    # def to_dict(self):
    #     task_dict = {
    #         "id": self.id,
    #         "title": self.title,
    #         "description": self.description,
    #         "is_complete": bool(self.completed_at)
    #     }
    #     if self.goal_id:
    #         task_dict["goal_id"] = self.goal_id
    #     return task_dict
        
        
    
    # @classmethod
    # def from_dict(cls, task_data):
    #     """
    #     Create a Task instance from a dictionary (e.g., request body).
    #     """
    #     # Handle the case where 'completed_at' might be passed as a string or datetime object
    #     completed_at = task_data.get("completed_at")
    #     if completed_at:
    #         completed_at = datetime.fromisoformat(completed_at) if isinstance(completed_at, str) else completed_at

    #     new_task = cls(
    #         title=task_data["title"],
    #         description=task_data["description"],
    #         completed_at=completed_at,
    #         goal_id=task_data.get("goal_id")
    #     )
    #     return new_task
    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "is_complete": bool(self.completed_at)
        }
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict

    @classmethod
    def from_dict(cls, task_data):
        is_complete = task_data.get("is_complete", False)
        completed_at = datetime.now() if is_complete else None

        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=completed_at,
            goal_id=task_data.get("goal_id")
        )
        return new_task
    

    