from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv(override=True)
app = Flask(__name__)

app.config['SECRET_KEY'] = 'hlkfjrijhfbekeihydndkvh'  # secure session data
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
postgre_url = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_DATABASE_URI"] = postgre_url.replace(
    'postgres:', 'postgresql:')

db = SQLAlchemy(app)
