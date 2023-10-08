from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Note
from . import db
import json

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html", user=current_user)


@views.route("/users")
def users():
    users = User.query.order_by("id")
    notes = Note.query.order_by("user_id")
    return render_template("users.html", user=current_user, users=users, notes=notes)


@views.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    if request.method == "POST":
        note = request.form.get("note")
        if note is None:
            flash("empty note", category="error")
        else:
            new_note = Note()
            new_note.text = note
            new_note.user_id = current_user.id
            db.session.add(new_note)
            db.session.commit()
            flash("note added", category="success")
    return render_template("notes.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)  # noteId is from index.js
    if note:
        if note.user_id == current_user.id:  # security check
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
