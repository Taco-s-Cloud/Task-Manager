from flask import Flask
from .routers import tasks
from .database import engine, Base
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    #CORS(app)
    CORS(app, resources={r"/*": {"origins": "https://taco-ui-1024364663505.us-central1.run.app"}})
    # Register blueprints
    app.register_blueprint(tasks.tasks_blueprint)

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    return app
