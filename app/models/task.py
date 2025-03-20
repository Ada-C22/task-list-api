from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[str]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")


    # from model to JSON
    def to_dict(self):
        if self.goal_id is None:
            return dict(
                    id=self.id,
                    title=self.title,
                    description=self.description,
                    is_complete=self.completed_at!=None
                    )
        else:
            return dict(
                    id=self.id,
                    title=self.title,
                    description=self.description,
                    is_complete=self.completed_at!=None,
                    goal_id=self.goal_id
                    )
    
    # from JSON to model
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"]
        )


   
   

   

