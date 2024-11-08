from app import create_app, db
from app.models.task import Task

my_app = create_app()
with my_app.app_context():
    db.session.add(Task(title="6 AM Yoga Session", description="Start the day with a 20-minute yoga session to improve flexibility, focus, and reduce stress.")),
    db.session.add(Task(title="Prepare Breakfast", description="Cook a healthy breakfast to fuel the day ahead, focusing on balanced nutrition.")),
    db.session.add(Task(title="Drive Kids to School", description="Drop the kids off at school at 8 AM, ensuring a smooth and safe start to their day.")),
    db.session.add(Task(title="Morning Cleaning Routine", description="Quick 15-minute cleaning session to organize the kitchen and living area.")),
    db.session.add(Task(title="Lunch Preparation", description="Prepare a nutritious lunch, considering leftovers or meal prepping for time efficiency.")),
    db.session.add(Task(title="Afternoon Cleaning: Tidy Up Workspace", description="Organize the workspace and put away any clutter to maintain a productive environment.")),
    db.session.add(Task(title="Pick Up Kids from School", description="Pick up the kids at 4 PM from school, ensuring a safe and timely trip.")),
    db.session.add(Task(title="Prepare Dinner", description="Cook a balanced dinner, involving the kids if possible to make it a fun family activity.")),
    db.session.add(Task(title="5:30 PM Journal Time", description="Spend a few minutes journaling to reflect on the day's experiences and set intentions for tomorrow.")),
    db.session.add(Task(title="Evening Cleaning: Kitchen and Living Area", description="Clean up the kitchen and tidy up the living area after dinner.")),
    db.session.add(Task(title="Family Time", description="Enjoy quality time with family, engaging in a shared activity or relaxing together.")),
    db.session.add(Task(title="Bedtime Routine", description="Prepare for a restful night's sleep with a calming routine, like reading or relaxing music.")),
    db.session.commit()
    