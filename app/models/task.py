from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .goal import Goal


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=None
    )
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    @property
    def is_complete(self):
        return self.completed_at is not None

    def mark_complete(self):
        self.completed_at = datetime.now()

    def mark_incomplete(self):
        self.completed_at = None

    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete
        }
    
    # Include goal_id if the task belongs to a goal
        if self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id
                
        return task_dict

    @classmethod
    def from_dict(cls, task_data):
        goal_id = task_data.get("goal_id") 
        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
            goal_id=goal_id  
        )

        return new_task
