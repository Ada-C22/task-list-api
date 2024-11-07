from app import create_app, db
from app.models.goal import Goal


my_app = create_app()
with my_app.app_context():
    db.session.add(Goal(title= "Get Fit"))
    db.session.add(Goal(title= "Be an Adult"))
    db.session.add(Goal(title= "Graduate ADA"))
    # db.session.add(Goal(title= ""))
    # db.session.add(Goal(title= ""))
    db.session.commit()


    # curl -X POST -H 'Content-Type: application/json' -d '{"name":"Felix","color":"black and white","personality":"wonderful"}' 'http://localhost:5000/cats' | json_p