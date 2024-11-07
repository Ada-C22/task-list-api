from app import create_app, db
from app.models.task import Task
from app.models.goal import Goal

my_app = create_app()
with my_app.app_context():
    db.session.add(Task(title="Task List API project",description="Unit 2 project due on Friday, Nov 8"))
    db.session.add(Task(title="Rewatch Recursion lecture",description="Part of Computer Science Fundamentals"))
    db.session.add(Task(title="Read Many-to-Many lecture on Learn",description="Lesson 10, part of the Building an API series"))
    db.session.add(Task(title="Grocery shopping at Sprouts",description="Check grocery list on phone notes for specifics"))
    db.session.add(Task(title="Hot girl walk",description="Get those steps in!!!"))

    db.session.add(Goal(title="Studying"))
    db.session.add(Goal(title="Errands"))
    db.session.add(Goal(title="Self-care"))
    db.session.commit()