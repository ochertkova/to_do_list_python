
import json
from src import app, db
from flask import Flask, jsonify, request, abort
from src.models import *
from datetime import datetime


def validate_auth(request):
    # Read Authorization header from request
    # Check formaat Bearer TOKEN
    # Decrypt TOKEN with env.secret, read user_id from the decrypted json
    if 'Authorization' in list(request.headers.keys()):
        bearer_token = request.headers.get('Authorization')[7:]
        db_user = db.session.query(User).filter_by(
            email=bearer_token).first()
        if db_user:
            return db_user.id
    abort(403)


@app.route('/todos', methods=['GET'])
def get_todos():
    statuses = ['NotStarted', 'OnGoing', 'Completed']
    user_id = validate_auth(request)
    if request.args.get('status') in statuses:
        db_result = db.session.query(Todo).filter_by(
            user_id=user_id, status=request.args.get('status'))
    else:
        db_result = db.session.query(Todo).filter_by(user_id=user_id)

    return jsonify([elem.to_dict() for elem in db_result])


@app.route('/todos', methods=['POST'])
def add_todo():
    user_id = validate_auth(request)
    todo = json.loads(request.data)
    todo["created"] = datetime.now()
    todo["updated"] = datetime.now()
    entry = Todo(todo['name'], todo["description"], user_id,
                 todo["created"], todo["updated"], todo["status"])
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict())


@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    user_id = validate_auth(request)
    update_data = json.loads(request.data)
    db_todo = db.session.query(Todo).get(id)

    if db_todo.user_id != user_id:
        abort(403)

    db_todo.updated = datetime.now()
    db_todo.name = update_data['name']
    db_todo.description = update_data["description"]
    db_todo.status = update_data["status"]
    db.session.commit()
    return jsonify(db_todo.to_dict())


@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    user_id = validate_auth(request)
    db_todo = db.session.query(Todo).get(id)

    if db_todo.user_id != user_id:
        abort(403)

    db.session.delete(db_todo)
    db.session.commit()
    return jsonify({'id': id})


@app.route('/users/signup', methods=['POST'])
def add_user():
    user = json.loads(request.data)
    user["created"] = datetime.now()
    user["updated"] = datetime.now()
    entry = User(user['email'], user["password"],
                 user["created"], user["updated"])
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry)
