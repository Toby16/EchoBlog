from EchoBlog_app import db
from datetime import datetime


class User(db.Model):
    """
    Model for 'user' table in database
    """
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(60), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password = db.Column(db.String(200))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):
        return "user -> '{}'".format(self.username)


class Post(db.Model):
    """
    Model for user's 'post' table in database
    """
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.String())
    timestamp = db.Column(
                    db.DateTime(), index=True,
                    default=datetime.utcnow
                )
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __repr__(self):
        if len(self.body) <= 20:
            return "post -> '{}'".format(self.body)
        return "post -> '{}'".format(self.body[:20] + "...")

