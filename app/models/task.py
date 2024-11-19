from sqlalchemy.orm import Mapped, mapped_column , relationship
from sqlalchemy import ForeignKey
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title : Mapped[str]
    description : Mapped [str]
    completed_at: Mapped[Optional[datetime]] 
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal : Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        is_complete_task= False
        if self.completed_at:
            is_complete_task = True
        
        task_dict = dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=is_complete_task,
            
        )
        if self.goal:
            task_dict["goal_id"] = self.goal.id
            
        return task_dict
        
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=None,
            goal_id=task_data.get("goal_id", None)
           
        )
    
   
    