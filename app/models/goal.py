from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.routes.utilities_routes import create_model, validate_model
from typing import Optional
from sqlalchemy import ForeignKey
# from app.models.task import Task
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship("Task",back_populates="goal")



    def to_dict(self):
        goal_as_dict = {}
        goal_as_dict["id"] = self.id
        goal_as_dict["title"] = self.title
        
        return goal_as_dict


    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(
            title=goal_data["title"]
        )
        return new_goal