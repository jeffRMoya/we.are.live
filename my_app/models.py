from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Event(db.Model):
    title = db.Column(db.String(200))
    data = db.Column(db.String(200))
    image = db.Column(db.String(300))
    date = db.Column(db.String(150))
    city = db.Column(db.String(100))
    website = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    id = db.Column(db.Integer, primary_key=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    avatar = db.Column(db.String(200))
    events = db.relationship('Event')
