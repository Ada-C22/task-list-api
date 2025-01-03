from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import List

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[List["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
        )

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"]
        )

