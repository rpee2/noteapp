from flask import Blueprint, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from . import db

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(400)
def not_found_error(error):
    return render_template('erreur/erreur.html', user=current_user, e='400'), 400


# https://flask-wtf.readthedocs.io/en/1.0.x/csrf/#customize-the-error-response
# @errors.errorhandler(CSRFError)
# def handle_csrf_error(error):
#     return render_template('erreur/erreur.html', user=current_user, e='400'), 400


@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('erreur/erreur.html', user=current_user, e='404'), 404


@errors.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('erreur/erreur.html', user=current_user, e='500'), 500


