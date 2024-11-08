from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.routes.utilities_routes import create_model, validate_model, check_for_completion
from typing import Optional
from sqlalchemy import ForeignKey
# from app.models.task import Task
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship("Task",back_populates="goal", lazy=True)
    # description=Mapped[str]
    # completed_at: Mapped[Optional[datetime]]=mapped_column(nullable = True)


    def to_dict(self):
        goal_as_dict = {}
        goal_as_dict["id"] = self.id
        goal_as_dict["title"] = self.title
        if self.tasks:
            task_ids=[]
            task_dictionaries = [task.to_dict() for task in self.tasks]
            for task in task_dictionaries: 
                task_id = task.get("id")
                task_ids.append(task_id)
            goal_as_dict["task_ids"] = task_ids
        else: 
            goal_as_dict["task_ids"] = []
        # task_as_dict["description"] = self.description
        # task_as_dict["is_complete"] = check_for_completion(Goal,self)
        
        return goal_as_dict



    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(
            title=goal_data["title"],
            # description=goal_data["description"],
            # completed_at=goal_data["completed_at"]
        )
        return new_goal