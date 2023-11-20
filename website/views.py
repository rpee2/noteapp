from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    jsonify,
    redirect,
    url_for,
    session,
    abort,
)
from flask_login import login_required, current_user
from .models import User, Note, Tag
from .forms import CustomTagForm
from datetime import datetime, timezone, timedelta
from sqlalchemy.sql import func
from . import db
import json


views = Blueprint("views", __name__)


def time_ago(date_modified):
    now = datetime.utcnow()
    time_difference = now - date_modified
    seconds_ago = (
        time_difference.total_seconds()
    )  # https://stackoverflow.com/questions/51652952/python-timedelta-seconds-vs-total-seconds
    if seconds_ago / 86400 >= 1:
        return ["day", int(seconds_ago / 86400)]
    elif seconds_ago / 3600 >= 1:
        return ["hour", int(seconds_ago / 3600)]
    else:
        return ["min", int(seconds_ago / 60)]


# inject tags to populate the sidebar tag filter thing
@views.context_processor
def inject_tags():
    available_tags = {}
    if current_user.is_authenticated:
        available_tags = (
            Tag.query.filter_by(user_id=current_user.id).order_by(Tag.order.asc()).all()
        )
    return dict(global_tags=available_tags)


@views.route("/", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        filtered_notes = []
        if request.args.get(
            "filter"
        ):  # hidden checkbox with name="filter" (this means that form was submitted and we are trying to find out if "filter" exists. If form was not submitted, filter would not exist)
            tags_id = request.args.getlist("filtered-tags")  # a list of tag IDs

            filtered_tags = []
            filtered_tags = Tag.query.filter(Tag.id.in_(tags_id)).all()
            if filtered_tags:  # != []
                session["filtered_tags_id"] = [
                    tag.id for tag in filtered_tags
                ]  # accessed in base.html
                session["filtered_tags_name"] = [
                    tag.name for tag in filtered_tags
                ]  # accessed in index.html
                session.modified = True

                # https://stackoverflow.com/questions/42334197/add-only-unique-values-to-a-list-in-python
                # filtered_notes = list(set(filtered_notes))

                filtered_notes = (
                    Note.query.join(Tag, Note.tags)
                    .filter(Tag.id.in_(session["filtered_tags_id"]))
                    .group_by(Note.id)
                    .having(
                        func.count(Tag.id.distinct())
                        == len(session["filtered_tags_id"])
                    )
                    .order_by(Note.date_modified.desc())
                    .all()
                )
                # this is how the query works, it's a little glonky but it works. if tags_id (which the user selected) is 1 and 2, the notes containing tags 1 and 2, notes containing 1 but not 2, notes containing 2 but not 1 and notes containing both 1 and 2 are filtered. (these notes can also contain other tags but since we filter only tags 1 and/or 2, the other tags are not chosen in the query). Then we group tags by the note. If the no. of tags in the note are greater than or equal to the tags in tags_id, those notes are filtered (having is filter for aggregate functions).
                # so for example, there is note-1-2, note-1-3, note-1, note-1-2-3.
                # Note-1-2 is selected because it has tags 1 and 2, which are in tags_id. The number of distinct tags in the note is 2, which is equal to the len of tags_id.
                # Note-1-3 is NOT selected because tag 3 is NOT in tags-id.
                # Note-1 is NOT selected - it passes the first filter because tag 1 is in tags_id. However it doesn't pass the 'having' because it only has 1 distinct tag.
                # Note-1-2-3 is selected because it has tags 1 and 2 which are in tags_id. The number of distinct tags in the note is also 2, because tag 3 is not in tags_id.
                # https://stackoverflow.com/questions/13349832/sqlalchemy-filter-to-match-all-instead-of-any-values-in-list
                # https://stackoverflow.com/questions/35414358/sqlalachmey-orm-filter-to-match-all-items-in-a-list-not-any
            else:
                session["filtered_tags_id"] = []
                session["filtered_tags_name"] = []
                session.modified = True
                # if filters were unselected, we got to reset the filters
                filtered_notes = (
                    Note.query.filter_by(user_id=current_user.id)
                    .order_by(Note.date_modified.desc())
                    .all()
                )

        elif session.get(
            "filtered_tags_id"
        ):  # for normal GET requests when form was not submitted, we check if there are any filtered_tags, if there are we continue to show them
            filtered_notes = (
                Note.query.join(Tag, Note.tags)
                .filter(Tag.id.in_(session["filtered_tags_id"]))
                .group_by(Note.id)
                .having(
                    func.count(Tag.id.distinct()) == len(session["filtered_tags_id"])
                )
                .order_by(Note.date_modified.desc())
                .all()
            )
        else:  # for scenarios when no filters are selected
            filtered_notes = (
                Note.query.filter_by(user_id=current_user.id)
                .order_by(Note.date_modified.desc())
                .all()
            )

        for note in filtered_notes:
            note.time_ago = time_ago(note.date_modified)
            note.date_created_strf = (
                note.date_created.replace(tzinfo=timezone.utc)
                .astimezone(tz=None)
                .strftime("%x")
            )  # ?? https://stackoverflow.com/questions/4563272/how-to-convert-a-utc-datetime-to-a-local-datetime-using-only-standard-library

        return render_template(
            "content/index.html", user=current_user, filtered_notes=filtered_notes
        )
    return render_template("landing.html", user=current_user)


@views.route("/note/new", methods=["GET", "POST"])
@views.route("/note/<note_id>", methods=["GET", "POST"])
@login_required
def note(note_id=None):
    user_tags = Tag.query.filter_by(user_id=current_user.id).all()

    if request.method == "GET":
        # retrieve all the info from the note db object and display it on the screen
        if note_id is None:
            new_note = Note()
            new_note.user_id = current_user.id
            db.session.add(new_note)
            db.session.commit()
            flash("note created", category="success")
            return redirect(url_for("views.note", note_id=new_note.id))
        else:
            current_note = Note.query.get_or_404(note_id)
            if (
                current_note.user_id == current_user.id
            ):  # very important (without this users can access other users' notes)
                note_tags = current_note.tags
                note_title = current_note.title
                note_body = current_note.body
                return render_template(
                    "content/note.html",
                    user=current_user,
                    note_title=note_title,
                    note_body=note_body,
                    js_note_tags=note_tags,  # tags belonging to the note
                    js_user_tags=user_tags,  # tags belonging to the user
                )
            else:
                abort(404)
    elif request.method == "POST":
        # retrieve all the info from the form and save it to the db
        current_note = Note.query.get_or_404(note_id)
        current_note.tags.clear()  # remove all previously saved tags on the note
        tags_id = request.form.get("note-tags")  # ['2,3,6']
        if (
            tags_id
        ):  # allow for when there are no tags because the code below assumes tags
            tags_id = tags_id.split(",")  # ['2','3','6'] (str)
            tags_id = [int(tag_id) for tag_id in tags_id]  # convert to int
            # I have to be clear about what I'm passing around. Append takes in the ORM object as the variable. So I can't append the id directly, such as, current_note.tags.id.append(tag) where tag is a int for the id. I have to query for the object before appending it.
            for tag_id in tags_id:
                tag = Tag.query.filter_by(id=tag_id).one_or_none()
                current_note.tags.append(tag)
        else:  # allow for when there were tags but user removes tags
            tags_id = []
            current_note.tags = tags_id
        current_note.title = request.form.get("note-title")
        current_note.body = request.form.get("note-body")
        current_note.date_modified = datetime.utcnow()
        # current_note.verified = True
        db.session.commit()
        flash("note saved", category="success")
        return redirect(url_for("views.note", note_id=current_note.id))
    # return render_template("content/note.html", user=current_user, tags=tags)


@views.route("/edit-tags", methods=["GET", "POST"])
@login_required
def edit_tags():
    tags = (
        Tag.query.filter_by(user_id=current_user.id)
        .order_by(Tag.order.asc(), Tag.order.asc())
        .all()
    )

    if request.method == "POST":
        # new_tags = request.form.to_dict()

        for k, v in request.form.items(
            multi=True
        ):  # https://stackoverflow.com/questions/58172414/iterate-over-keys-and-all-values-in-multidict
            # print(f"{k}, {v}")
            # e.g.
            # parent-1, hobbies
            # child-6-1, dance
            # child-7-1, guitar
            # child-8-1, minecraft
            # parent-2, books
            # child-9-2, reviews
            # new-parent-32768, y32768
            # new-child-1-32768, x1
            # new-parent-32769, y32769
            # new-child-2-32769, x2
            # https://stackoverflow.com/questions/73606635/flask-forms-handle-multiple-identical-form-fields
            if k.split("-")[1] == "parent":  # new parent
                counter = 1
                new_parent_tag = Tag(name=v, level=1, user_id=current_user.id)
                db.session.add(new_parent_tag)
                db.session.commit()
                # this breaks if there are parent tags with the same name
                parent = Tag.query.filter_by(name=v).first()
                for key, value in request.form.items(multi=True):
                    if (
                        key.split("-")[-1] == k.split("-")[-1]
                        and key.split("-")[1]
                        != "parent"  # prevent parent from adding itself
                    ):
                        new_child_tag = Tag(
                            name=value,
                            level=2,
                            order=counter,
                            parent_tag=parent.id,
                            user_id=current_user.id,
                        )
                        db.session.add(new_child_tag)
                        db.session.commit()
                        print(f"{counter},{value}")
                        counter += 1

            elif k.split("-")[0] == "parent":  # existing parent
                parent_id = k.split("-")[-1]
                counter = 1
                existing_parent_tag = Tag.query.filter_by(id=parent_id).first()
                existing_parent_tag.name = v
                db.session.commit()
                for key, value in request.form.items(multi=True):
                    if (
                        key.split("-")[-1] == parent_id
                        and key.split("-")[0] != "parent"
                    ):
                        if key.split("-")[0] != "new":
                            child_id = key.split("-")[1]
                            existing_child_tag = Tag.query.filter_by(
                                id=child_id
                            ).first()
                            existing_child_tag.name = value
                            existing_child_tag.order = counter
                            db.session.commit()
                            print(f"{counter},{value}")
                            counter += 1
                        elif (
                            key.split("-")[1] != "parent"
                        ):  # prevent adding itself as child
                            new_child_tag = Tag(
                                name=value,
                                level=2,
                                order=counter,
                                parent_tag=parent_id,
                                user_id=current_user.id,
                            )
                            db.session.add(new_child_tag)
                            db.session.commit()
                            print(f"{counter},{value}")
                            counter += 1

            elif k == "tags-to-delete":
                tags_to_delete = v.split(",")
                # print(tags_to_delete)
                # ['parent-2', 'child-8-1', 'child-7-1', '']
                for tag in tags_to_delete:
                    if tag:
                        delete_id = tag.split("-")[1]
                        tag_to_delete = Tag.query.get(delete_id)
                        db.session.delete(tag_to_delete)
                        db.session.commit()
                        # print(delete_id)
                        # 2 8 7

        flash("saved", category="success")
        return redirect(url_for("views.edit_tags"))
    return render_template("content/edit-tags.html", user=current_user, tags=tags)


@views.route("/delete-note", methods=["POST"])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)  # noteId is from index.js
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("note deleted", category="success")
    return jsonify({})
