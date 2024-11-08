from app import create_app, db
from app.models.task import Task
from app.models.goal import Goal

my_app = create_app()

with my_app.app_context():

    # Add tasks
    db.session.add(Task(title="Set Up Development Environment", description="", completed_at=None)),
    db.session.add(Task(title="Learn Basic Syntax in Python", description="", completed_at=None)),
    db.session.add(Task(title="Complete a Python Data Types Tutorial", description="", completed_at=None)),
    db.session.add(Task(title="Write a Simple 'Hello, World!' Program", description="", completed_at=None)),
    db.session.add(Task(title="Understand Variables and Data Types", description="", completed_at=None)),
    db.session.add(Task(title="Practice with Basic Operators in Python", description="", completed_at=None)),
    db.session.add(Task(title="Create a Simple Calculator Program", description="", completed_at=None)),
    db.session.add(Task(title="Learn Conditional Statements (if/else)", description="", completed_at=None)),
    db.session.add(Task(title="Explore Loops (for and while loops)", description="", completed_at=None)),
    db.session.add(Task(title="Build a Basic To-Do List Program", description="", completed_at=None)),
    db.session.add(Task(title="Get Familiar with Functions and Modules", description="", completed_at=None)),
    db.session.add(Task(title="Complete Coding Exercises on Lists and Dictionaries", description="", completed_at=None)),
    db.session.add(Task(title="Work with Strings and String Manipulation", description="", completed_at=None)),
    db.session.add(Task(title="Learn About Error Handling and Exceptions", description="", completed_at=None)),
    db.session.add(Task(title="Explore Object-Oriented Programming Concepts", description="", completed_at=None)),
    db.session.add(Task(title="Plan a 5K Training Schedule", description="Create a weekly training plan with incremental goals", completed_at=None)),
    db.session.add(Task(title="Buy Proper Running Shoes", description="Get fitted for supportive shoes at a running store", completed_at=None)),
    db.session.add(Task(title="Run/Walk for 20 Minutes 3x This Week", description="Start with a run/walk routine to build endurance", completed_at=None)),
    db.session.add(Task(title="Increase Running Distance by 0.5K", description="Gradually add more distance each week", completed_at=None)),
    db.session.add(Task(title="Join a Local Running Group", description="Find motivation and accountability by running with others", completed_at=None)),
    db.session.add(Task(title="Run a Practice 5K", description="Complete a practice 5K to gauge readiness before race day", completed_at=None)),
    db.session.add(Task(title="Drink 8 Glasses of Water Daily", description="Track water intake to stay hydrated", completed_at=None)),
    db.session.add(Task(title="Prepare a Weekly Meal Plan", description="Plan balanced meals for the week ahead", completed_at=None)),
    db.session.add(Task(title="Get 7-8 Hours of Sleep Each Night", description="Establish a consistent sleep schedule", completed_at=None)),
    db.session.add(Task(title="Exercise for 30 Minutes 5x a Week", description="Incorporate regular exercise into your routine", completed_at=None)),
    db.session.add(Task(title="Limit Screen Time Before Bed", description="Avoid screens 1 hour before bed for better sleep", completed_at=None)),
    db.session.add(Task(title="Practice Daily Meditation or Mindfulness", description="Take 10 minutes a day to relax and refocus", completed_at=None)),

    # Add goals
    db.session.add(Goal(title="Learn to Code")),
    db.session.add(Goal(title="Run a 5k")),
    db.session.add(Goal(title="Routines")),

    # Commit the session to save changes to the database
    db.session.commit()

print("Database seeded successfully!")