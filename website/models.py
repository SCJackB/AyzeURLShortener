from . import db
from flask_login import UserMixin


# Create a database model for storing urls
class urls(db.Model):
    # create an id for the stored urls
    id = db.Column(db.Integer, primary_key=True)
    # store the long url
    longurl = db.Column(db.String())
    # store the shortened url
    shorturl = db.Column(db.String())
    # set the user id to the logged in user
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# Create a databse model for storing users
class User(db.Model, UserMixin):
    # Create a UID
    id = db.Column(db.Integer, primary_key=True)
    # store the users email
    email = db.Column(db.String(150), unique=True)
    # Store a hash of the users password
    password = db.Column(db.String(150))
    # store the username
    username = db.Column(db.String(150))
    # link the urls created by a user to that user specifically
    urls = db.relationship("urls")
