from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task
from app.middleware.auth import verify_token

# Create a Blueprint for task routes
tasks_blueprint = Blueprint("tasks", __name__)

# GET: Retrieve all tasks
@tasks_blueprint.route("/tasks", methods=["GET"])
@verify_token
def get_tasks():
    try:
        db: Session = next(get_db())
        tasks = db.query(Task).all()
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "due_date": task.due_date,
                "completed": task.completed,
            }
            for task in tasks
        ]
        return jsonify(task_list), 200
    except Exception as e:
        print(f"Error retrieving tasks: {e}")
        return jsonify({"error": str(e)}), 500

# POST: Save a new task
@tasks_blueprint.route("/tasks", methods=["POST"])
@verify_token
def save_task():
    data = request.get_json()
    try:
        db: Session = next(get_db())
        new_task = Task(
            title=data.get("title"),
            description=data.get("description"),
            due_date=data.get("due_date"),
            completed=data.get("completed", False),
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return jsonify({"message": "Task added successfully", "task": data}), 201
    except Exception as e:
        print(f"Error saving task: {e}")
        return jsonify({"error": str(e)}), 500

# PUT: Update an existing task
@tasks_blueprint.route("/tasks/<int:task_id>", methods=["PUT"])
@verify_token
def update_task(task_id):
    data = request.get_json()
    try:
        db: Session = next(get_db())
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.title = data.get("title", task.title)
            task.description = data.get("description", task.description)
            task.due_date = data.get("due_date", task.due_date)
            task.completed = data.get("completed", task.completed)
            db.commit()
            db.refresh(task)
            return jsonify({"message": "Task updated"}), 200
        else:
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        print(f"Error updating task: {e}")
        return jsonify({"error": str(e)}), 500

# DELETE: Remove a task
@tasks_blueprint.route("/tasks/<int:task_id>", methods=["DELETE"])
@verify_token
def delete_task(task_id):
    try:
        db: Session = next(get_db())
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            db.delete(task)
            db.commit()
            return jsonify({"message": "Task deleted"}), 200
        else:
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        print(f"Error deleting task: {e}")
        return jsonify({"error": str(e)}), 500
