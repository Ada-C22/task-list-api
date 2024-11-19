from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="goal")

    def to_dict(self):     
        goal_as_dict = {
            "id": self.id,
            "title": self.title,
        }

        if  self.tasks: 
            goal_as_dict = {
            "id": self.id,
            "title": self.title,
            "tasks": [task.id for task in self.tasks] 
        }
            
        return goal_as_dict
