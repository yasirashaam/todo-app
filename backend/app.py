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

@app.route('/add-test')
def add_test():
    task = {
        "title": "My First Task",
        "category": "General",
        "completed": False
    }
    tasks.insert_one(task)
    return "Test task added"

# GET tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = []
    for task in tasks.find():
        task['_id'] = str(task['_id'])
        all_tasks.append(task)
    return jsonify(all_tasks)

# POST new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = {
        "title": data["title"],
        "category": data["category"],
        "completed": False
    }
    tasks.insert_one(task)
    return jsonify({"message": "Task added"})

# DELETE task
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    tasks.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Task deleted"})

# Run app
if __name__ == "__main__":
    app.run(debug=True)