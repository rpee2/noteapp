from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db" # https://stackoverflow.com/a/61850514 


def create_app():
    app = Flask(__name__)
    app.secret_key = "jamescharles"

    # initialize db
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .error_handler import errors

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(errors, url_prefix="/")
    
    from .models import User

    with app.app_context():
        db.drop_all() # comment out when I'm not working on the db
        db.create_all() # create all does not recreate tables already present in the target database (database.db)

    
    # initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login" 
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app