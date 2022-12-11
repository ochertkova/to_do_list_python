
import json
from src import app, db
from flask import Flask, jsonify, request, abort
from src.models import *
from datetime import datetime


def validate_auth(request):
    # Read Authorization header from request
    # Check formaat Bearer TOKEN
    # Decrypt TOKEN with env.secret, read user_id from the decrypted json
    if 'Email' in list(request.headers.keys()):
        db_user = db.session.query(User).filter_by(
            email=request.headers.get('Email')).first()
        if db_user:
            return db_user.id
    abort(403)


@app.route('/todos', methods=['GET'])
def get_todos():
    user_id = validate_auth(request)
    return jsonify([elem.to_dict() for elem in db.session.query(Todo).filter_by(user_id=user_id)])


@ app.route('/todos', methods=['POST'])
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
