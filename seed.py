from app import create_app, db
from app.models.task import Task

my_app = create_app()
with my_app.app_context():
    db.session.add(Task(title="Cooking", description="Cooking biriyani", completed_at=None)),
    db.session.add(Task(title="Baking", description="Baking rainbow cupcakes", completed_at=None)),
    db.session.add(Task(title="Hiking", description="Hiking mount-Rainier", completed_at=None)),
    db.session.add(Task(title="Painting", description="Painting tropical flowers", completed_at=None)),
    db.session.add(Task(title="Grocery", description="Doing weekly grocery", completed_at=None)),
    db.session.add(Task(title="Coding", description="Coding python", completed_at=None)),
    db.session.add(Task(title="Learning", description="Learning a new language", completed_at=None)),
    db.session.add(Task(title="Watching", description="Watching 5 comedy movies", completed_at=None)),
    db.session.add(Task(title="Reading", description="Reading a 10 books", completed_at=None)),
    db.session.add(Task(title="Traveling", description="Traveling to all the US National parks", completed_at=None)),
    db.session.add(Task(title="Volunteering", description="Volunteering at elementary school", completed_at=None)),
    db.session.add(Task(title="Planting", description="Planting 20 tropical indoor plants", completed_at=None)),
    db.session.add(Task(title="Writing", description="Writing a children's book", completed_at=None)),
    db.session.add(Task(title="Walking", description="Walking through a hiking trail with friends", completed_at=None)),
    db.session.add(Task(title="Playing", description="Playing Piano", completed_at=None)),
    db.session.add(Task(title="Crafting", description="Making decorative crafts", completed_at=None)),
    db.session.add(Task(title="Driving", description="Drive through mounatains and caves", completed_at=None)),
    db.session.commit()