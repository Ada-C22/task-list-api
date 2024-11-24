from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from app import db
from typing import Optional
class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(nullable=True, default=None)
    # is_complete: Mapped[bool] = mapped_column(nullable=True) 
    goal_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("goal.id"), nullable=True)
    goal = relationship("Goal", back_populates="tasks")
    
    
    @property
    def is_complete(self) -> bool:
        return self.completed_at is not None
        
    def to_dict(self):
        """Regular to_dict without goal_id for most routes"""
        is_complete_value = False if self.completed_at is None else True
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete,
        }

    def to_dict_with_goal(self):
        """Special method that includes goal_id for goal-related routes"""
        is_complete_value = False if self.completed_at is None else True
        return {
            "id": self.id,
            "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete_value
        } 

  


    
 
       