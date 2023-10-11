from EchoBlog_app import app
from flask import render_template, flash, redirect, url_for
from EchoBlog_app.forms import LoginForm


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


@app.route("/login", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    """
    Route for user login
    """
    form = LoginForm()  # implement flask-forms on the frontend

    if form.validate_on_submit():  # run all validations on input fields
        print(form.data)
        flash("Login requested for user: {}, remember_me: {}".format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))

    return render_template("login.html", form=form, title="Sign In")
