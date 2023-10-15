from EchoBlog_app import app, db
from flask import (render_template, flash, redirect, url_for, request)
from EchoBlog_app.forms import LoginForm, RegistrationForm
from EchoBlog_app.models import User
from flask_login import (current_user, login_user,
                         logout_user, login_required)
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/index")
@app.route("/index/")
@login_required
def index():
    # Basic set up EchoBlog application
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
            posts=posts
    )


@app.route("/login", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    """
    Route for user login
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()  # implement flask-forms on the frontend

    if form.validate_on_submit():  # run all validations on input fields
        #  print(form.data)
        user = None

        try:
            if "@" in form.username.data:
                # to confirm if input is an email and query the database
                user = User.query.filter_by(email=form.username.data).first()
            
            # This code is ignored if input is an email and an account has been found
            if user is None:
                user = User.query.filter_by(username=form.username.data).first()
        except Exception as e:
            raise

        if (user is None) or (user.check_password(form.password.data) is False):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        
        # If no errors occur, log-in the user and redirect to index page
        login_user(user, remember=form.remember_me.data)

        # expose the contents of the query string in a friendly dictionary format
        # and get the value of the key - 'next'
        next_page = request.args.get("next")

        
        if (not next_page) or (url_parse(next_page)["netloc"] != ""):
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", form=form, title="Sign In")


@app.route("/logout")
@app.route("/logout/")
def logout():
    """
    endpoint to logout user
    """
    logout_user()
    return redirect(url_for("index"))


@app.route("/register")
@app.route("/register/")
def register():
    """
    view function for user account registeration
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(u)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)
