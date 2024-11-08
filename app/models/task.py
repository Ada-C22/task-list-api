from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=None)
    is_complete: Mapped[bool] = mapped_column(default=False)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_as_dict = {
            "id" : self.id,
            "title" : self.title,
            "description": self.description,
            "is_complete": self.is_complete
        }

        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id
            
        return task_as_dict