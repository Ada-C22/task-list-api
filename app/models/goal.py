from sqlalchemy.orm import Mapped, mapped_column,relationship
from ..db import db
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .task import Task

class Goal(db.Model):
    __tablename__ = 'goal'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[Optional[list["Task"]]] = relationship(back_populates="goal")

    @classmethod
    def from_dict(cls, data):
        # Creates a Task instance from a dictionary
        
        return cls(
            title=data["title"],
        )

    def to_dict(self, include_name=True, tasks_ids=False):
        # Converts a Task instance to a dictionary
        goal_dict = {

            "id": self.id,
            "title": self.title,
        }

        if tasks_ids:
            tasks_ids_list = [task.id for task in self.tasks]
            goal_dict["task_ids"] = tasks_ids_list
            goal_dict.pop("title")
        
        if include_name:
            return {Goal.__name__.lower(): goal_dict}
        
        return goal_dict

