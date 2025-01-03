from flask import Flask
from .routes.task_routes import tasks_bp
from .routes.goal_routes import goals_bp
from .db import db, migrate
from .models import task
from .models import goal
import os

def create_app(config=None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/task_list_api_development'

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(tasks_bp)
    app.register_blueprint(goals_bp)

    return app