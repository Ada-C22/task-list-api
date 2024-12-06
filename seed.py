from app import create_app, db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime


my_app = create_app()

with my_app.app_context():

    goal1 = Goal(title="Health and Well-being")
    goal2 = Goal(title="Team Collaboration")
    goal3 = Goal(title="Skill Development")
    goal4 = Goal(title="Project Planning")

    db.session.add_all([goal1, goal2, goal3, goal4])
    db.session.commit()
    
    tasks = [
        Task(title="Go on my daily walk 🏞", description="Notice something new every day", completed_at=None, goal_id=goal1.id),
        Task(title="Yoga Practice", description="30 minutes of morning yoga", completed_at=None, goal_id=goal1.id),
        Task(title="Team Meeting", description="Attend the weekly team sync-up meeting", completed_at=datetime(2024, 10, 2, 9, 0), goal_id=goal2.id),
        Task(title="Code Review", description="Review code for recent pull requests", completed_at=datetime(2024, 10, 3, 11, 15), goal_id=goal2.id),
        Task(title="Client Call", description="Discuss requirements with the client", completed_at=datetime(2024, 10, 4, 15, 0), goal_id=goal2.id),
        Task(title="Update Documentation", description="Add details to the API documentation", completed_at=datetime(2024, 10, 5, 10, 30), goal_id=goal3.id),
        Task(title="Research on Tech Trends", description="Research new technology trends for the next project", completed_at=datetime(2024, 10, 6, 13, 0), goal_id=goal3.id),
        Task(title="Design New Feature", description="Design wireframes for new app feature", completed_at=datetime(2024, 10, 7, 16, 45), goal_id=goal3.id),
        Task(title="Project Roadmap", description="Create roadmap for the new project", completed_at=None, goal_id=goal4.id),
        Task(title="Sprint Planning", description="Plan tasks for upcoming sprint", completed_at=None, goal_id=goal4.id)
    ]

    db.session.add_all(tasks)
    db.session.commit()
