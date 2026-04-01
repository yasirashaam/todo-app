from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

# Initialize app
app = Flask(__name__)
CORS(app)

# Database connection
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
tasks_collection = db["tasks"]

# Helper function
def serialize_task(task):
    return {
        "_id": str(task["_id"]),
        "title": task.get("title"),
        "category": task.get("category"),
        "completed": task.get("completed", False),
        "dueDate": task.get("dueDate")
    }

# Home route
@app.route('/')
def home():
    return jsonify({
        "message": "🚀 Backend is running successfully"
    })

# GET all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = [serialize_task(task) for task in tasks_collection.find()]
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CREATE task
@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json

        # Validation
        if not data.get("title"):
            return jsonify({"error": "Title is required"}), 400

        task = {
            "title": data["title"],
            "category": data.get("category", "General"),
            "completed": False,
            "dueDate": data.get("dueDate"),
            "priority": data.get("priority", "Medium")
        }

        result = tasks_collection.insert_one(task)

        return jsonify({
            "message": "Task created successfully",
            "id": str(result.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE task (complete / undo)
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    try:
        data = request.json

        tasks_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )

        return jsonify({"message": "Task updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE task
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    try:
        tasks_collection.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "Task deleted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run server
if __name__ == "__main__":
    app.run(debug=True)