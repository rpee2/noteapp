from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import re
from . import db  # from the init.py
from .models import User
from .forms import LoginForm, SignupForm, ChangePasswordForm, AccountSettingsForm, UpdateProfileForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form=LoginForm()

    if form.validate_on_submit():
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
            flash("logged in", category="success")
            login_user(user, remember=True)
            return redirect(url_for("views.home"))
        
        return redirect(url_for("auth.login")) 

    return render_template("auth/login.html", user=current_user, form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("logged out", category="success")
    return redirect(url_for("views.home"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # The tos checkbox is not part of the SignupForm, I should include it so I don't have to do this inconsistent code here and on the HTML
    tos_checkbox = request.form.get("checkedTos") 

    form=SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password1 = form.password.data
        password2 = form.confirm_password.data
        
        # if checkbox is not checked (default), we get false. if checked, we get true.
        beta_checkbox = False
        if form.hasBeta.data:
            beta_checkbox = True

        user = User.query.filter_by(
            email=email
        ).first()  # search if the email provided already exists in the db

        if email and name and password1 and password2 is not None:
            if user:
                flash("user already exists", category="error")
            elif not tos_checkbox:
                flash("accept Terms of Service to signup", category="error")
            elif re.search(r"^\S+@{1}\S+\.{1}\S+", email) is None:
                flash("invalid email", category="error")
            elif len(name) <= 1:
                flash("invalid name", category="error")
            elif password1 != password2:
                flash("passwords don't match", category="error")
            elif len(password1) < 7:
                flash("password must at least 7 characters", category="error")
            else:
                # saving all the form data into the database
                new_user = User()
                new_user.email = email
                new_user.name = name
                new_user.password = generate_password_hash(password1, method="scrypt") 
                new_user.hasBeta = beta_checkbox
                db.session.add(new_user)
                db.session.commit()

                flash("account created", category="success")
                return redirect(url_for("auth.login"))
        else:
            flash("missing input", category="error")
        
        return redirect(url_for("auth.signup")) 

    return render_template("auth/signup.html", user=current_user, form=form)


@auth.route("/account-settings", methods=["GET", "POST"])
@login_required
def account_settings():
    form=AccountSettingsForm()
    if request.method == "GET":
        if current_user.hasBeta: 
            form.hasBeta.data = True

    if form.validate_on_submit():
        password = form.password.data
        if check_password_hash(current_user.password, password) is True:  
            user = current_user
            if form.submit.data:
                user.hasBeta = form.hasBeta.data
                db.session.commit()
                flash("saved settings", category="success")
            elif form.delete_account.data:
                db.session.delete(user)
                db.session.commit()
                flash("account deleted", category="success")
                return redirect(url_for("views.home"))
        else:
            flash("wrong password", category="error")
        return redirect(url_for("auth.account_settings")) 
    return render_template("auth/account-settings.html", user=current_user, form=form)


# update user email and name 
@auth.route("/update-profile", methods=["GET", "POST"])
@login_required
def update_profile():
    form = UpdateProfileForm()

    # inject the form with current user email and name
    # another method is in update-profile.html, use a "value = {{ user.email }}" in the input box
    if request.method == "GET":
        form.email.data = current_user.email 
        form.name.data = current_user.name  
        # form.submit.label.text = 'Update'

    if form.validate_on_submit():
        user = current_user
        user.email = form.email.data
        user.name = form.name.data
        db.session.commit()
        flash("profile updated", category="success")

        # display new info (not needed when you redirect the page)
        # form.email.data = current_user.email
        # form.name.data = current_user.name   
        return redirect(url_for("auth.update_profile")) 
        
    return render_template("auth/update-profile.html", user=current_user, form=form)


@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form=ChangePasswordForm()

    if form.validate_on_submit():
        old_password = form.old_password.data
        if check_password_hash(current_user.password, old_password) is not True: 
            flash("wrong password", category="error") 
        elif form.new_password.data != form.confirm_password.data: 
            flash("new password does not match", category="error")
        else:
            user = current_user
            user.password = generate_password_hash(form.new_password.data, method="scrypt") 
            db.session.commit()
            flash("password changed", category="success")
        return redirect(url_for("auth.change_password")) 
    return render_template("auth/change-password.html", user=current_user, form=form)


