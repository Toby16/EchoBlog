from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from logging.handlers import RotatingFileHandler
import logging
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Object to manage database migration
login = LoginManager(app)  # Object to manage user logge-in state
login.login_view = "login"  # 'login' is the view function that handles logins
# bootstrap = Bootstrap(app) # To implement Bootstrap3 on the frontend
# moment = Moment(app)  # to incorporate moment.js into the application

from EchoBlog_app import routes, models, errors


if not app.debug:
    """
    Logging errors to a log file
    """
    if not os.path.exists("logs"):
        os.mkdir("logs")

    # limiting the size of the log file to 10KB
    # and keeping the last ten log files as backup.
    file_handler = RotatingFileHandler("logs/EchoBlog.log", maxBytes=10240, backupCount=10)

    # using a format that includes the timestamp,
    # the logging level, the message and the source file
    # and line number from where the log entry originated.
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("EchhoBlog startup")


