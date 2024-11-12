from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal

class Task(db.Model):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)   # Title column required
    description: Mapped[str] = mapped_column(nullable=False)    # Description column required
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=None)
    is_complete: Mapped[Optional[bool]] = False
    goal_id: Mapped[Optional[int]] = mapped_column((ForeignKey("goal.id")), default=None)
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    @classmethod
    def from_dict(cls, data):
        """Creates a Task instance from a dictionary"""
        
        return cls(
            title=data["title"],
            description=data["description"],
            completed_at=data.get("completed_at") # Use .get() since "completed_at" is optional
        )

    def to_dict(self, include_name=True, goal_id=False):
        """Converts a Task instance to a dictionary"""
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)  # Convert to boolean for completeness
        }
        if goal_id:
            task_dict["goal_id"] = self.goal.id

        if include_name:
            return {Task.__name__.lower(): task_dict}
        
        return task_dict
    
    