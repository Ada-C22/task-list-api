from app import create_app, db
from app.models.task import Task

my_app = create_app()
with my_app.app_context():
    db.session.add(Task(title="Do laundry", description="Wash, dry, and fold", completed_at="2024-11-20T19:45:00Z"))
    db.session.add(Task(title="Buy groceries", description="Milk, eggs, bread, and vegetables", completed_at="2024-11-21T14:00:00Z"))
    db.session.add(Task(title="Prepare presentation", description="Finalize slides for the team meeting", completed_at="2024-11-22T10:30:00Z"))
    db.session.add(Task(title="Call the plumber", description="Schedule a visit to fix the kitchen sink", completed_at="2024-11-23T16:15:00Z"))
    db.session.add(Task(title="Workout", description="30-minute cardio and strength training", completed_at="2024-11-24T07:00:00Z"))
    db.session.add(Task(title="Finish book", description="Complete reading 'The Great Gatsby'", completed_at="2024-11-25T20:45:00Z"))
    db.session.add(Task(title="Plan trip", description="Research flights and accommodations for vacation", completed_at="2024-11-26T12:00:00Z"))
    db.session.add(Task(title="Clean the car", description="Wash and vacuum the car interior", completed_at="2024-11-27T09:30:00Z"))
    db.session.add(Task(title="Pay utility bills", description="Electricity, water, and internet bills", completed_at="2024-11-28T18:00:00Z"))
    db.session.add(Task(title="Cook a special dinner", description="Try out a new recipe for family dinner", completed_at="2024-11-29T19:00:00Z"))
    db.session.add(Task(title="Organize the closet", description="Sort clothes and donate unused items", completed_at="2024-11-30T15:00:00Z"))
    db.session.commit()