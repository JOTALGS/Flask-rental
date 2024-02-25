from datetime import datetime
from unwrap import db, login_manager
from flask_login import UserMixin
from flask import flash
import uuid

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    lastname = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.firstname}','{self.lastname}', '{self.email}','{self.id}')"


class Property(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    price = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    location = db.relationship('Location', backref='properties')

    def __repr__(self):
        return f"Property('{self.name}', '{self.price}')"

class Location(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Location(city='{self.city}', country='{self.country}')"