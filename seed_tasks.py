from app import create_app, db
from app.models.task import Task


my_app = create_app()
with my_app.app_context():
    db.session.add(Task(title= "Exercise", description="take a yoga class"))
    db.session.add(Task(title= "Wash day", description="Try out new condidtioner"))
    db.session.add(Task(title= "Survive", description="You can do it!"))
    # db.session.add(Task(title= "", description=""))
    # db.session.add(Task(title= "", description=""))
    db.session.commit()


    # curl -X POST -H 'Content-Type: application/json' -d '{"name":"Felix","color":"black and white","personality":"wonderful"}' 'http://localhost:5000/cats' | json_p