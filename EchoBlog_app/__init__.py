from flask import Flask

app = Flask(__name__)

from EchoBlog_app import routes
