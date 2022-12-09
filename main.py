from src import db, app
from src.models import *
from src.api import *


db.create_all()  # create a database before the app is run

if __name__ == "__main__":  # run web server only if this file runs directly
    app.run(debug=True)
