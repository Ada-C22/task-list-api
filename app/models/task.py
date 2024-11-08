from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ..db import db
from sqlalchemy import ForeignKey
from typing import Optional
from app.models.goal import Goal
from app.routes.route_utilities import check_complete

class Task(db.Model):
    
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"], description=task_data["description"], completed_at=task_data["completed_at"])
        return new_task
    
    def to_dict(self):
        return dict(
        id=self.id,
        goal_id=self.goal_id,
        title=self.title,
        description=self.description,
        is_complete=check_complete(self.completed_at)
        )