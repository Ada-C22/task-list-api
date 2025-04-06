from flask import Flask
from .db import db, migrate
from .models import task, goal
from app.routes.task_routes import bp as tasks_bp
from app.routes.goal_routes import bp as goals_bp
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if test_config:
        # Merge `config` into the app's configuration
        # to override the app's default settings for testing
        app.config.update(test_config)

    # Initialize app with SQLAlchemy and Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(tasks_bp)
    app.register_blueprint(goals_bp)

    return app
