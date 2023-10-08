from flask import Blueprint, render_template, request, flash, redirect, url_for
import re
from . import db  # from the init.py
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("user does not exist", category="error")
        elif password is None:
            flash("password not entered", category="error")
        elif check_password_hash(user.password, password) is False:
            flash("incorrect password", category="error")
        else:
            flash("logged in successfully", category="success")
            login_user(user, remember=True)
            return redirect(url_for("views.home"))

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("you are logged out", category="success")
    return redirect(url_for("views.home"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # email = str(email)
        # firstName = str(firstName)
        # password1 = str(password1)
        # password2 = str(password2)
        user = User.query.filter_by(
            email=email
        ).first()  # search if the email provided already exists in the db

        if email and firstName and password1 and password2 is not None:
            if user:
                flash("user already exists", category="error")
            elif re.search(r"^\S+@{1}\S+\.{1}\S+", email) is None:
                flash("invalid email", category="error")
            elif len(firstName) <= 1:
                flash("invalid name", category="error")
            elif password1 != password2:
                flash("passwords don't match", category="error")
            elif len(password1) < 7:
                flash("password must at least 7 characters", category="error")
            else:
                # saving all the form data into the database
                new_user = User()
                new_user.email = email
                new_user.firstName = firstName
                new_user.password = generate_password_hash(password1, method="sha256")
                db.session.add(new_user)
                db.session.commit()

                flash("account created", category="success")
                login_user(new_user, remember=True)
                return redirect(url_for("views.home"))
        else:
            flash("multiple missing information", category="error")

    return render_template("signup.html", user=current_user)
