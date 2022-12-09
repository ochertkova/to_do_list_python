from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)
app = Flask(__name__)

app.config['SECRET_KEY'] = 'hlkfjrijhfbekeihydndkvh'  # secure session data
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRESQL_URL"]

db = SQLAlchemy(app)
