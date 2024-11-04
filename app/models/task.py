from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .goal import Goal

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(default=None, nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        goal_id = task_data.get("goal_id")
        new_task = cls(title=task_data["title"],
                            description=task_data["description"],
                            completed_at=task_data.get("completed_at", None),
                            goal_id=goal_id)
                            
        return new_task

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = bool(self.completed_at)
        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id

        # if self.goal:
        #     task_as_dict["goal"] = self.goal.title

        return task_as_dict