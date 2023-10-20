from EchoBlog_app import app, db
from flask import (render_template, flash,
                   redirect, url_for, request)
from EchoBlog_app.forms import (LoginForm, RegistrationForm,
                                EditProfileForm, EmptyForm, PostForm)
from EchoBlog_app.models import User, Post
from flask_login import (current_user, login_user,
                         logout_user, login_required)
from werkzeug.urls import url_parse
from datetime import datetime


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/index/", methods=["GET", "POST"])
@login_required
def index():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('Your post is now live!')
        return redirect(url_for('index'))
    else:
        print(form.validate_on_submit())

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
            posts=posts,
            form=form
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


@app.route("/register", methods=["GET", "POST"])
@app.route("/register/", methods=["GET", "POST"])
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

        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/user/<username>")
@app.route("/user/<username>/")
@login_required
def user(username):
    """
    view function for user profile page
    """
    username = str(username)
    user = User.query.filter_by(username=username).first_or_404()

    posts = [
        {"author": user, "body": "Hello World!, I code in Python"},
        {"author": user, "body": "Using Flask Framework to build web applications"}
    ]
    form = EmptyForm()

    return render_template("user.html", user=user, posts=posts, form=form, title="Profile")


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        """
        including 'db.session.add()' is not necessary here because,
        when you reference current_user,
        Flask-Login will invoke the user loader callback function,
        which will run a database query that will put the target user in the database session
        """
        db.session.commit()


@app.route("/edit_profile", methods=["GET", "POST"])
@app.route("/edit_profile/", methods=["GET", "POST"])
@login_required
def edit_profile():
    """
    view function to edit user profile
    """
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved successfully!")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", title="Edit Profile", form=form)


@app.route("/follow/<username>", methods=["POST"])
@app.route("/follor/<username>/", methods=["POST"])
@login_required
def follow(username):
    form = EmptyForm()

    if form.validate.on_submit():
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))

        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))

        current_user.follow(user)
        db.session.commit()
        flash("You are now following {}".format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for("index"))


@app.route("/unfollow/<username>", methods=["POST"])
@app.route("/unfollow/<username>/", methods=["POST"])
@login_required
def unfollow(username):
    form = EmptyForm()

    if form.validate.on_submit():
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash("User {} not found.".format(username))
            return redirect(url_for("index"))

        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))

        current_user.unfollow(user)
        db.session.commit()
        flash('You have unfollowed {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
