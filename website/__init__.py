from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from .constants import csp


db = SQLAlchemy()
csrf = CSRFProtect()
talisman = Talisman()


def create_app():
    app = Flask(__name__)
    # for development 
    app.config.from_mapping(
        FLASK_DEBUG = True,
        SECRET_KEY = "james_charles",
        SQLALCHEMY_DATABASE_URI = "sqlite:///housing.db",
        SQLALCHEMY_TRACK_MODIFICATIONS = True,
        SQLALCHEMY_ECHO = True
    )
    # for production
    app.config.from_object('config.Config') 

    db.init_app(app)
    csrf.init_app(app)
    talisman.init_app(app)
    talisman.content_security_policy = csp

    from .models import User

    from .views import views
    from .auth import auth
    from .error_handler import errors

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(errors, url_prefix="/")

    with app.app_context():
        # db.drop_all()  # comment out when I'm not working on the db
        db.create_all()  # create all does not recreate tables already present in the target database (database.db)

    # initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
