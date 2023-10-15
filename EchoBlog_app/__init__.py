from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Object to manage database migration
login = LoginManager(app)  # Object to manage user logge-in state
login.login_view = "login"  # 'login' is the view function that handles logins

from EchoBlog_app import routes, models
