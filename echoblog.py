from EchoBlog_app import app, db
from EchoBlog_app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    """
    a shell context that adds the database instance and models
    to the flask shell session
    """
    return {"db": db, "User": User, "Post": Post}

if __name__ == "__main__":
    app.run(debug=True)
