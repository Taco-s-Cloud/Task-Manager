from flask import Flask
from .routers import tasks
from .database import engine, Base

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(tasks.tasks_blueprint)

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    return app