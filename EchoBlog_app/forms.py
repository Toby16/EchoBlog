
from flask_wtf import FlaskForm
from wtforms import (
        StringField, SubmitField,
        PasswordField, BooleanField
    )
from wtforms.validators import (
        DataRequired, Email,
        EqualTo, ValidationError
    )
from EchoBlog_app.models import User


class LoginForm(FlaskForm):
    # Get user login credentials
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log in")

class RegistrationForm(FlaskForm):
    # Get user details to create a new account
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    retype_password = PasswordField("Re-type Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Create account")

    def validate_username(self, username):
        """
        method to check if username already exists
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username not available!")


    def validate_email(self, emai):
        """
        method to check if email already exists
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address!")
