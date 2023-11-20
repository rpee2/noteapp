from . import db  # from init.py
from flask_login import UserMixin
from sqlalchemy.sql import func
from dataclasses import dataclass

# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/models/
# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/#insert-update-delete


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)  # nullable=False
    password = db.Column(db.String(32))  # this is the sha256 hash not the password
    name = db.Column(db.String(64))
    hasBeta = db.Column(db.Boolean())
    tags = db.relationship("Tag", backref="user")
    notes = db.relationship("Note", backref="user")

    def __repr__(self):
        return f"<User: {self.name}>"


# https://www.digitalocean.com/community/tutorials/how-to-use-many-to-many-database-relationships-with-flask-sqlalchemy
tags_x_notes = db.Table(
    "tags_x_notes",
    db.Column("note_id", db.Integer, db.ForeignKey("note.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
)


# https://www.reddit.com/r/flask/comments/8f3bom/sqlalchemy_query_as_dict/
# https://www.reddit.com/r/flask/comments/vll4xu/af_how_to_turn_flask_sqlalchemy_query_results/
@dataclass
class Tag(db.Model):
    __tablename__ = "tag"
    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("user.id"))
    name: str = db.Column(db.String(128))
    level: int = db.Column(db.Integer)
    order: int = db.Column(db.Integer)
    parent_tag: int = db.Column(db.Integer, db.ForeignKey("tag.id"), default=None)
    # You use the backref parameter to add a back reference that behaves like a column to the Tag model. This way, you can access the tag’s notes via tag.notes and the tags of a note via note.tags.
    # only need to do the relationship once
    notes = db.relationship("Note", secondary=tags_x_notes, backref="tags")

    def __repr__(self):
        return f"<Tag: {self.name}>"


# https://www.youtube.com/watch?v=47i-jzrrIGQ
class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(256), default="")
    body = db.Column(db.Text, default="")
    date_created = db.Column(
        db.DateTime(timezone=True), default=func.now()
    )  # altenative to func.now() is datetime.utcnow
    date_modified = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"<Note: {self.title}>"
