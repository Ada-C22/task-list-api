from flask import Flask
from importlib import import_module
from .db import db, migrate
from .models import task, goal
import os
from app.routes.task_routes import tasks_bp
from app.routes.goal_routes import goals_bp 
from dotenv import load_dotenv
load_dotenv()

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config.update(config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    migrate.init_app(app, db)

    # app.register_blueprint(tasks_bp)
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(goals_bp,url_prefix='/goals')
    
    @app.route('/')
    def home():
        return {"message": "Welcome to Task API"}, 200
    
    return app
