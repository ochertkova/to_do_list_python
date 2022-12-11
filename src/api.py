
import json
from src import app, db
from flask import Flask, jsonify, request, abort
from src.models import *
from datetime import datetime
import bcrypt
import jwt
import os


def encode_token(token):
    '''Encodes auth token using TOKEN_SECRET from environment'''
    return jwt.encode(token, os.environ['TOKEN_SECRET'], algorithm='HS256')


def validate_auth(request):
    # Read Authorization header from request
    # Decrypt TOKEN with env.secret, read user_id from the decrypted json
    try:
        # any error here leads to 403
        if 'Authorization' in list(request.headers.keys()):
            encoded_token = request.headers.get('Authorization')[7:]
            token = jwt.decode(encoded_token,
                               os.environ['TOKEN_SECRET'], algorithms=['HS256'])
            return token['user_id']
    except:
        pass
    abort(403)


@app.route('/api/v1/todos', methods=['GET'])
def get_todos():
    statuses = ['NotStarted', 'OnGoing', 'Completed']
    user_id = validate_auth(request)
    if request.args.get('status') in statuses:
        db_result = db.session.query(Todo).filter_by(
            user_id=user_id, status=request.args.get('status'))
    else:
        db_result = db.session.query(Todo).filter_by(user_id=user_id)

    return jsonify([elem.to_dict() for elem in db_result])


@app.route('/api/v1/todos', methods=['POST'])
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


@app.route('/api/v1/todos<int:id>', methods=['PUT'])
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


@app.route('/api/v1/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    user_id = validate_auth(request)
    db_todo = db.session.query(Todo).get(id)

    if not db_todo:
        abort(404)
    if db_todo.user_id != user_id:
        abort(403)

    db.session.delete(db_todo)
    db.session.commit()
    return jsonify({'id': id})


@app.route('/api/v1/signup', methods=['POST'])
def add_user():
    user = json.loads(request.data)
    user["created"] = datetime.now()
    user["updated"] = datetime.now()

    password_hash = bcrypt.hashpw(
        bytes(user["password"], 'UTF-8'), bcrypt.gensalt()).decode('UTF-8')

    entry = User(user['email'], password_hash,
                 user["created"], user["updated"])
    db.session.add(entry)
    db.session.commit()
    return '', 201


@app.route('/api/v1/signin', methods=['POST'])
def login_user():
    login_data = json.loads(request.data)
    db_user = db.session.query(User).filter_by(
        email=login_data["email"]).first()

    # check received password from request  against password in DB
    if db_user and bcrypt.checkpw(login_data["password"].encode('UTF-8'), db_user.password.encode('UTF-8')):
        # return encoded token for user
        return encode_token({'user_id': db_user.id}), 200

    abort(403)


@app.route('/api/v1/changePassword', methods=['PUT'])
def change_password():
    user_id = validate_auth(request)

    pwd_data = json.loads(request.data)
    db_user = db.session.query(User).get(user_id)

    db_user.password = bcrypt.hashpw(
        bytes(pwd_data["newPassword"], 'UTF-8'), bcrypt.gensalt()).decode('UTF-8')
    db.session.commit()
    return '', 204
