from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from flask import abort, make_response

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def obj_to_dict(self):
        goal_as_dict = {}
        goal_as_dict["id"] = self.id
        goal_as_dict["title"] = self.title

        return goal_as_dict


    @classmethod
    def obj_from_dict(cls, goal_data):
        title = goal_data.get("title", None)

        if not title:
            response = {"details": "Invalid data"}
            abort(make_response(response, 400))

        new_goal = cls(
            title=title
        )

        return new_goal
    