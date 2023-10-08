from . import db  # from init.py
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True) # nullable=False
    password = db.Column(db.String(32))
    firstName = db.Column(db.String(64))
    notes = db.relationship("Note")

    def __repr__(self):
        return "<Name %r>" % self.firstName


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(16384))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #altenative to func.now() is datetime.utcnow
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
