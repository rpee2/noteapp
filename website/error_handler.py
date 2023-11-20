from flask import Blueprint, render_template
from flask_login import current_user
from . import db

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('erreur/erreur.html', user=current_user, e='404'), 404


@errors.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('erreur/erreur.html', user=current_user, e='500'), 500


