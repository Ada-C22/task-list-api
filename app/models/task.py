from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from sqlalchemy import ForeignKey
from typing import Optional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = bool(self.completed_at)
        #task_as_dict["goal_id"] = self.goal.id if self.goal else None

        if self.goal:
            task_as_dict["goal_id"] = self.goal.id

        return task_as_dict
    
    @classmethod
    def from_dict(cls, task_data):
        # Use get() to fetch values that could be undefined to avoid raising an error
        goal_id = task_data.get("goal_id")

        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
            goal_id=goal_id
        )

        return new_task

