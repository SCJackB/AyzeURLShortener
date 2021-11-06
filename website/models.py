from . import db
from flask_login import UserMixin


class urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longurl = db.Column(db.String())
    shorturl = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    urls = db.relationship("urls")
