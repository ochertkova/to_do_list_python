from datetime import datetime
from . import db


class Todo(db.Model):  # type: ignore
    """
    A class used to represent a Todo note and create a table in DB

    Attributes
    ----------
    id: int
        Unique identifier
    name: str
        Name of the todo item
    description: str
        Description of the toto item
    user id: int
        Id of the user who owns this todo item
    created: datetime
        When the item is created
    updated: datetime
        When the item is last updated
    status: str
        An enum of either: NotStarted, OnGoing, Completed

    Methods
    -------
    to_dict(self)
        Returns a class instance as a dictionary
    """

    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    status = db.Column(db.String(64))

    def __init__(self, name, description, user_id, created, updated, status):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.created = created
        self.updated = updated,
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'status': self.status,
            'created': self.created,
            'updated': self.updated
        }


class User(db.Model):  # type: ignore
    """
    A class used to represent a User and create a table in DB

    Attributes
    ----------
    id: int
        Unique identifier
    email: str
        Email address
    password: str
        Password
    created: datetime
        When the user is created
    updated: datetime
        When the user is last updated
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    todos = db.relationship('Todo')

    def __init__(self, email, password, created, updated):
        self.email = email
        self.password = password
        self.created = created
        self.updated = updated
