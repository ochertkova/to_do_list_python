from src import create_app, db
from src.models import *

app = create_app()
db.create_all()

if __name__ == "__main__":  # run web server only if this file runs directly
    app.run(debug=True)
