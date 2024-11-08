from app import create_app, db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

my_app = create_app()

with my_app.app_context():
    
    goal1 = Goal(title="Complete Python Project")
    goal2 = Goal(title="Learn SQLAlchemy")

    db.session.add(goal1)
    db.session.add(goal2)

    db.session.add(Task(
        title="Write Python code",
        description="Complete the coding part of the project.",
        completed_at=datetime(2024, 11, 7, 14, 30),
        goal=goal1
    ))
    db.session.add(Task(
        title="Test the code",
        description="Run tests to ensure functionality.",
        completed_at=None, 
        goal=goal1
    ))
    db.session.add(Task(
        title="Read SQLAlchemy documentation",
        description="Understand SQLAlchemy ORM basics.",
        completed_at=datetime(2024, 11, 6, 10, 0),
        goal=goal2
    ))
    db.session.add(Task(
        title="Practice SQLAlchemy queries",
        description="Experiment with CRUD operations in SQLAlchemy.",
        completed_at=None, 
        goal=goal2
    ))

    db.session.commit()
