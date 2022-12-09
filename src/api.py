
import json
from src import app, db
from flask import Flask, jsonify, request, abort
from src.models import *
from datetime import datetime
import jsonpickle


@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonpickle.encode([item for item in db.session.query(Todo).all()])


@app.route('/todos/add', methods=['POST'])
def add_todo():
    todo = json.loads(request.data)
    todo["created"] = datetime.now()
    todo["updated"] = datetime.now()
    entry = Todo(todo['name'], todo["description"], todo["user_id"],
                 todo["created"], todo["updated"], todo["status"])
    print(jsonpickle.encode(entry))
    db.session.add(entry)
    db.session.commit()
    return jsonpickle.encode(entry)


@app.route('/users/signup', methods=['POST'])
def add_user():
    user = json.loads(request.data)
    user["created"] = datetime.now()
    user["updated"] = datetime.now()
    entry = User(user['email'], user["password"],
                 user["created"], user["updated"])
    db.session.add(entry)
    db.session.commit()
    return jsonpickle.encode(entry)
