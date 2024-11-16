from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db
from datetime import datetime 

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[str] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey('goal.id'))
    goal: Mapped[Optional['Goal']] = relationship(back_populates='tasks')
    

    def to_dict(self):
        return dict(
        id=self.id,
        title=self.title,
        description=self.description,
        is_complete=bool(self.completed_at),
        goal_id=self.goal.id if self.goal else None
        )
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(
            title=task_data['title'],
            description=task_data['description'],
            goal_id=task_data.get('goal_id',None)
            )
        return new_task
