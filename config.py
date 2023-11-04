import os

# main directory of the application
basedir_ = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or ("sqlite:///" + os.path.join(basedir_, "app.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # FOR PAGINATION
    POSTS_PER_PAGE = 15

