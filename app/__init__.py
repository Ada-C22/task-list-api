from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from .db import db, migrate
from .models import task, goal
from .routes.task_routes import tasks_bp
from .routes.slack_routes import slack_bp
from .routes.goal_routes import goals_bp
import os

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings for testing
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(tasks_bp)
    app.register_blueprint(slack_bp)
    app.register_blueprint(goals_bp)

    return app

# from flask import Flask
# from .db import db, migrate
# from .models import task, goal
# from .routes.task_routes import tasks_bp
# import os

# def create_app(config=None):
#     app = Flask(__name__)

#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

#     if config:
#         # Merge `config` into the app's configuration
#         # to override the app's default settings for testing
#         app.config.update(config)

#     db.init_app(app)
#     migrate.init_app(app, db)

#     # Register Blueprints here
#     app.register_blueprint(tasks_bp)

#     return app

