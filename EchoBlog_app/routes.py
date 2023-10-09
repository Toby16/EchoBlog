from EchoBlog_app import app
from flask import render_template


@app.route("/")
@app.route("/index")
@app.route("/index/")
def index():
    # Basic set up EchoBlog application
    user = {
        "username": "test_username",
        "email": "test@example.com"
    }
    posts = [
        {
            "author": {"username": "John"},
            "body": "Beautiful day in Portland!"
        },
        {
            "author": {"username": "Susan"},
            "body": "The Avengers movie was so cool!"
        }
    ]

    return render_template(
            "index.html",
            title="Home Page",
            user=user,
            posts=posts
    )
