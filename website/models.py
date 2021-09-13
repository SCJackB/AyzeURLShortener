from . import db
from flask_login import UserMixin

class urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longUrl = db.Column(db.String(10000))
    shortUrl = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    urlRealtionship = db.relationship('urls')