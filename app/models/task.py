from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(nullable=True)
    is_complete: Mapped[bool] = mapped_column(nullable=True,default=False)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_dict = {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "is_complete" : self.is_complete
        }
        
        if self.goal_id:
            task_dict['goal_id'] = self.goal_id
        
        return task_dict


    @classmethod
    def from_dict(cls, request_body):
        return cls(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body.get("completed_at") # use get.() to return None if no input 
        )
