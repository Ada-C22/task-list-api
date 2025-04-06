from sqlalchemy.orm import Mapped, mapped_column, relationship # type: ignore
from ..db import db
from ..routes.task_routes import validate_task
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")


    def check_goal_tasks(self):
        tasks_assigned  = []
        if self.tasks:
            for task in self.tasks:
                task = validate_task(task.id)
                tasks_assigned.append(task.to_nested_dict())
        
        return tasks_assigned

    def to_dict(self):
        goal_to_dict = {}
        goal_to_dict["id"] = self.id
        goal_to_dict["title"] = self.title
        return goal_to_dict
    
    def to_nested_dict(self):
        goal_to_dict = {}
        goal_to_dict["id"] = self.id
        goal_to_dict["title"] = self.title
        if not self.check_goal_tasks():
            goal_to_dict["tasks"] = []
        else:
            goal_to_dict["tasks"] = self.check_goal_tasks()
        
        return goal_to_dict
