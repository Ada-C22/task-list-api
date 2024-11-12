from sqlalchemy.orm import Mapped, mapped_column, relationship
from .task import Task
from ..db import db
from typing import List

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="goal")

    def to_dict(self):
        goal_as_dict = {
            "id": self.id,
            "title": self.title,
            "tasks": [task.to_dict() for task in self.tasks]  # Include tasks in the goal's dict
        }
        return goal_as_dict

    @classmethod
    def from_dict(cls, goal_data):
        return cls(title=goal_data["title"])

    def add_tasks(self, task_ids: List[int]):
        tasks = Task.query.filter(Task.id.in_(task_ids)).all()
        for task in tasks:
            task.goal_id = self.id  # Assign each task's goal_id
        db.session.commit()