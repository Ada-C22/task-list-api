from flask import Flask
from .db import db, migrate
import os
from .models import goal
from .models import task
from .routes.task_routes import tasks_bp
from .routes.goal_routes import goals_bp

from flask_cors import CORS

def create_app(config=None):
    app = Flask(__name__)

    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(tasks_bp)
    app.register_blueprint(goals_bp)

    return app