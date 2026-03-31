from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
tasks = db["tasks"]

@app.route('/')
def home():
    return "Backend is running"

# ✅ GET tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = []
    for task in tasks.find():
        task['_id'] = str(task['_id'])
        all_tasks.append(task)
    return jsonify(all_tasks)

# ✅ ADD task (with due date)
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = {
        "title": data["title"],
        "category": data["category"],
        "completed": False,
        "dueDate": data.get("dueDate")  # NEW
    }
    tasks.insert_one(task)
    return jsonify({"message": "Task added"})

# ✅ DELETE task
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    tasks.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Deleted"})

# ✅ UPDATE task (complete / undo)
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    data = request.json
    tasks.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )
    return jsonify({"message": "Updated"})

if __name__ == "__main__":
    app.run(debug=True)