from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task

# Create a Blueprint for task routes
tasks_blueprint = Blueprint('tasks', __name__)

# GET and POST: Handle all tasks
@tasks_blueprint.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    try:
        db: Session = next(get_db())

        if request.method == 'POST':
            # Process incoming task data
            data = request.get_json()
            new_task = Task(
                title=data.get('title'),
                description=data.get('description'),
                due_date=data.get('due_date'),
            )
            db.add(new_task)
            db.commit()
            db.refresh(new_task)
            return jsonify({"message": "Task added successfully", "task": new_task.to_dict()}), 201

        elif request.method == 'GET':
            # Retrieve tasks
            tasks = db.query(Task).all()
            return jsonify([task.to_dict() for task in tasks]), 200

    except Exception as e:
        print(f"Error handling tasks: {e}")
        return jsonify({"error": str(e)}), 500

# PUT: Update an existing task
@tasks_blueprint.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    try:
        db: Session = next(get_db())
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.due_date = data.get('due_date', task.due_date)
            db.commit()
            db.refresh(task)
            return jsonify({"message": "Task updated", "task": task.to_dict()}), 200
        else:
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        print(f"Error updating task: {e}")
        return jsonify({"error": str(e)}), 500

# DELETE: Remove a task
@tasks_blueprint.route("/tasks/<int:task_id>", methods=["DELETE"])
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
