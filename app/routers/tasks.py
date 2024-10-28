from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task

# Define the blueprint for tasks
tasks_blueprint = Blueprint("tasks", __name__)

# GET: Retrieve all tasks
@tasks_blueprint.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        db: Session = next(get_db())
        tasks = db.query(Task).all()
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "due_date": task.due_date,
            }
            for task in tasks
        ]
        return jsonify(task_list), 200
    except Exception as e:
        print(f"Error retrieving tasks: {e}")
        return jsonify({"error": str(e)}), 500

# Additional route handlers for POST, PUT, and DELETE follow a similar pattern