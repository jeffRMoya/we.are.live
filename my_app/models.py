from . import db
# gives user object specific items for logging in
from flask_login import UserMixin
from sqlalchemy.sql import func

# creates db models
# allows the mapping of data to these objects and allows them to be stored in db
# columns are created for data to be stored in tables
# primary keys are unique identifiers and once set, will be auto incremented when objects created


class Event(db.Model):
    title = db.Column(db.String(200))
    data = db.Column(db.String(200))
    image = db.Column(db.String(300))
    date = db.Column(db.String(150))
    city = db.Column(db.String(100))
    website = db.Column(db.String(300))
    # foreign key is a primary key from another data table
    # in this case it's what relates Event to User
    # so 'user_id' in Event will match the 'id' in User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    id = db.Column(db.Integer, primary_key=True)

# UserMixin allows the use of current_user later on


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # unique=True prevents multiple users from having the same email
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    avatar = db.Column(db.String(200))
    events = db.relationship('Event')
