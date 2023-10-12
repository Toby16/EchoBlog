from EchoBlog_app import db


class User(db.Model):
    """
    Model for 'user' table in database
    """
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(60), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password = db.Column(db.String(200))

    def __repr__(self):
        return "user -> '{}'".format(self.username)
