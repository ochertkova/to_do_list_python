from src import create_app

app = create_app()

if __name__ == "__main__":  # run web server only if this file runs directly
    app.run(debug=True)
