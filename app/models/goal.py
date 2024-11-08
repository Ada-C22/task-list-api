from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")
    
    def goal_dict(self):
        goal_as_dict = {}
        goal_as_dict["id"] = self.id
        goal_as_dict["title"] = self.title
        
        # if self.tasks:
        #     goal_as_dict["tasks"] = [task.task_dict() for task in self.tasks]
        # else:
        #     goal_as_dict["tasks"] = []
        
        return goal_as_dict
        
