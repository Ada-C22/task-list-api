from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from typing import Optional
from flask import make_response, abort
from sqlalchemy import ForeignKey

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    completed_at: Mapped[Optional[datetime]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id")) 
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")


    # book object to dict representation
    def obj_to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        if self.goal:
            task_as_dict["goal_id"] = self.goal.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = True if self.completed_at is not None else False

        return task_as_dict
    
    @classmethod
    # create instance from request body
    def obj_from_dict(cls, task_data):
        title = task_data.get("title", None)
        description = task_data.get("description", None)

        if not title or not description:
            response = {"details": "Invalid data"}
            abort(make_response(response, 400))

        new_task = cls(
            title=title,
            description=description,
            completed_at=task_data.get("completed_at", None)
            
        )

        return new_task