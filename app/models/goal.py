from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from app.routes.route_utilities import create_model

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        response = {
            "id": self.id,
            "title": self.title
        }
        return response
    
    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(title=goal_data["title"])
        return new_goal
