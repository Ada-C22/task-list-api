from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import db


class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    tasks = relationship('Task', back_populates='goal', cascade='all, delete-orphan')

    def to_dict(self, no_tasks=True):
        result = {"id": self.id, "title": self.title, }
        if not no_tasks:
            tasks = []
            for task in self.tasks:
                tasks.append(task.to_dict())
            result["tasks"] = tasks
        return result

    def from_dict(self, data:dict[str, any]):
        if id in data:
            self.id = data.get("id")
        if "title" in data:
            self.title = data["title"]
        return self
