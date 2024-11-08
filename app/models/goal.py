from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[List["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        goal_to_dict = {
            "id": self.id,
            "title": self.title,
            }
    
        if self.tasks:
            goal_to_dict["tasks"] = [task.to_dict() for task in self.tasks]

        return goal_to_dict
    
    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(title=goal_data["title"])
        return new_goal

