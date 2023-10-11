from flask_wtf import FlaskForm
from wtforms import (
        StringField, SubmitField,
        PasswordField, BooleanField
    )
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    # Get user login credentials
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log in")
