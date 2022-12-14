
import json
from src import app, db
from flask import jsonify, request, abort
from src.models import *
from datetime import datetime
import bcrypt
import jwt
import os


def forbidden(msg):
    """This function returns message for 403 response code in JSON format"""
    return jsonify({'msg': msg}), 403


def not_found(msg):
    """This function returns message for 404 response code in JSON format"""
    return jsonify({'msg': msg}), 404


def encode_token(token):
    """This function encodes auth token using TOKEN_SECRET from the environment"""
    return jwt.encode(token, os.environ['TOKEN_SECRET'], algorithm='HS256')


def validate_auth(request):
    """This function validates user authentication from request and returns user_id"""
    try:
        # any error here leads to 403
        if 'Authorization' in list(request.headers.keys()):
            # Read bearer token from Authorization header in request
            encoded_token = request.headers.get('Authorization')[7:]
            token = jwt.decode(encoded_token,
                               os.environ['TOKEN_SECRET'], algorithms=['HS256'])  # Decrypt TOKEN with env.secret, read user_id from the decrypted json
            return token['user_id']
    except:
        pass
    message = 'Authentication failed'
    fail_response = jsonify(message)
    fail_response.status_code = 403
    return abort(fail_response)


@app.route('/api/v1/todos', methods=['GET'])
def get_todos():
    """This function returns list of todo items.

    Optionally, a status query param can be included to return only items of specific status: NotStarted, OnGoing, Completed.
    If not present, return all items"""

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
    """This function creates a new todo item"""

    user_id = validate_auth(request)
    todo = json.loads(request.data)
    todo["created"] = datetime.now()
    todo["updated"] = datetime.now()
    entry = Todo(todo['name'], todo["description"], user_id,
                 todo["created"], todo["updated"], todo["status"])
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict())


@app.route('/api/v1/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    """This function updates a todo item"""

    user_id = validate_auth(request)
    update_data = json.loads(request.data)
    db_todo = db.session.query(Todo).get(id)

    if db_todo.user_id != user_id:  # check if user accesses their own todos
        message = 'Can not access this Todo'
        return forbidden(message)

    db_todo.updated = datetime.now()
    db_todo.name = update_data["name"]
    db_todo.description = update_data["description"]
    db_todo.status = update_data["status"]
    db.session.commit()
    return jsonify(db_todo.to_dict())


@app.route('/api/v1/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    """This function deletes a todo item"""

    user_id = validate_auth(request)
    db_todo = db.session.query(Todo).get(id)

    if not db_todo:
        message = 'Todo not found'
        return not_found(message)

    if db_todo.user_id != user_id:
        message = 'Can not access this Todo'
        return forbidden(message)

    db.session.delete(db_todo)
    db.session.commit()
    return jsonify({'id': id})


@app.route('/api/v1/signup', methods=['POST'])
def add_user():
    """This function adds a new user using email & password"""

    user = json.loads(request.data)
    user["created"] = datetime.now()
    user["updated"] = datetime.now()
    # check if user already exists
    if db.session.query(User).filter_by(email=user["email"]).first():
        message = 'This email is already registered'
        return forbidden(message)

    # generate password hash
    password_hash = bcrypt.hashpw(
        bytes(user["password"], 'UTF-8'), bcrypt.gensalt()).decode('UTF-8')

    try:
        entry = User(user['email'], password_hash,
                     user["created"], user["updated"])
        db.session.add(entry)
        db.session.commit()
        return '', 201
    except:
        message = 'Unable to add this user'
        return forbidden(message)


@app.route('/api/v1/signin', methods=['POST'])
def login_user():
    """This function logins user using email & password. 

    The system will return the encoded token that can be used to call the APIs that follow"""

    login_data = json.loads(request.data)
    db_user = db.session.query(User).filter_by(
        email=login_data["email"]).first()

    # check received password from therequest against password in DB
    if db_user and bcrypt.checkpw(login_data["password"].encode('UTF-8'), db_user.password.encode('UTF-8')):
        # return encoded token for user
        return encode_token({'user_id': db_user.id}), 200

    message = 'Password is incorrect. Try again'
    return forbidden(message)


@app.route('/api/v1/changePassword', methods=['PUT'])
def change_password():
    """This function changes user's password"""

    user_id = validate_auth(request)

    pwd_data = json.loads(request.data)
    db_user = db.session.query(User).get(user_id)

    db_user.password = bcrypt.hashpw(
        bytes(pwd_data["newPassword"], 'UTF-8'), bcrypt.gensalt()).decode('UTF-8')
    db_user.updated = datetime.now()
    db.session.commit()
    return '', 204
