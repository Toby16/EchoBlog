from EchoBlog_app import (db, login)
from datetime import datetime
from werkzeug.security import (generate_password_hash, check_password_hash)
from flask_login import UserMixin
from hashlib import md5

# self-referential many-to-many relationship that keeps track of followers
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    """
    Model for 'user' table in database
    """
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(60), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password = db.Column(db.String(200))  # stores password hash
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        "User", secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"), lazy="dynamic")

    def __repr__(self):
        return "user -> '{}'".format(self.username)

    def set_password(self, password):
        """
        Set hash value of password inputed
        """
        self.password = generate_password_hash(password)
        print("password hash:", self.password)

    def check_password(self, password):
        """
        Verify password with hash value
        """
        return check_password_hash(self.password, password)

    def avatar(self, size):
        from random import randint
        """
        method to create profile photo for users using Gravatar third-service
        """
        digest_ = md5(self.email.lower().encode("utf-8")).hexdigest()

        # image_gravatar_dict = {0: "robohash", 1: "retro", 2: "wavatar", 3: "monsterid", 4: "identicon"}
        # rand_gravatar = image_gravatar_dict[randint(0, 4)]

        # return the URL of the user's avatar image, scaled to the requested size in pixels
        # return "https://www.gravatar.com/avatar/{}?d={}&s={}".format(digest_, rand_gravatar, size)
        return "https://www.gravatar.com/avatar/{}?d={}&s={}".format(digest_, "robohash", size)

    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count() > 0

  
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())



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
        if len(self.body) <= 60:
            return "post -> '{}'".format(self.body)
        return "post -> '{}'".format(self.body[:60] + "...")


@login.user_loader
def load_user(id):
    """
    loader function to help the application in loading a user
    """
    return User.query.get(int(id))
