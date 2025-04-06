import os

from dotenv import load_dotenv
from flask import Flask

from .db import db, migrate
from .models import task, goal
from .routes.goal_routes import goal_bp
from .routes.task_routes import tasks_bp
from flask_cors import CORS

load_dotenv()


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    app.config['CORS_HEADERS'] = 'Content-Type'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings for testing
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(goal_bp)

    # Register Blueprints here

    return app
