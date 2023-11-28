from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    StringField,
    TextAreaField,
    EmailField,
    PasswordField,
    SubmitField,
    HiddenField,
    ValidationError,
    FieldList,
    Form,
    FormField,
)
from wtforms.validators import DataRequired, EqualTo, Length


# some forms don't have validators because I use custom loops to display the flash message. 

class LoginForm(FlaskForm):
    email = EmailField()
    password = PasswordField()
    submit = SubmitField("Submit")


class SignupForm(FlaskForm):
    email = EmailField()
    name = StringField()
    password = PasswordField()
    confirm_password = PasswordField()
    hasBeta = BooleanField("Enable Quantum Precognition")
    submit = SubmitField("Submit")


class AccountSettingsForm(FlaskForm):
    hasBeta = BooleanField("Enable Quantum Precognition")
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField("Submit")
    delete_account = SubmitField("Delete Account")


class UpdateProfileForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    update = SubmitField("Update")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(validators=[DataRequired()])
    new_password = PasswordField(
        validators=[
            DataRequired(),
            Length(min=7),
            # EqualTo("confirm_password", message="passwords do not match"),
        ],
    )
    confirm_password = PasswordField(validators=[DataRequired()])
    submit = SubmitField("Submit")


class NoteForm(FlaskForm):
    tag_search = StringField("Tags")
    note_tags = StringField()
    note_title = StringField("Title")
    note_body_delta = HiddenField()
    note_body_html = HiddenField()
    note_body_text = HiddenField()
    save = SubmitField("Save")


# https://www.youtube.com/watch?v=DqumX6deRR8 (learning how to create a dynamic form)
# class TagFormElement(Form):
#     tag = StringField()


# class CustomTagForm(FlaskForm):
#     tag = FieldList(FormField(TagFormElement), min_entries=0, max_entries=15)  # 15x15
#     update = SubmitField("Update")
