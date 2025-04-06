from sqlalchemy.orm import Mapped, mapped_column, relationship # type: ignore
from ..db import db
from datetime import datetime
from sqlalchemy import ForeignKey # type: ignore
from typing import Optional

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] # = completed_at if completed_at is not None

    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks") 

    
    def to_dict(self):
        if not self.completed_at:
            is_complete = False
        else:
            is_complete = True
        
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=is_complete
            )
    
    def to_nested_dict(self):
        if not self.completed_at:
            is_complete = False
        else:
            is_complete = True
        
        task_dictionary = dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=is_complete
            )
        
        if self.goal_id:
            task_dictionary["goal_id"] = self.goal_id

        return task_dictionary




