from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="goal")

    def goal_dict(self):
        return dict(
            id=self.id,
            title=self.title
        )

