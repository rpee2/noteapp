from os import environ, path
from dotenv import load_dotenv

BASEDIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASEDIR, ".env"))


class Config:
    FLASK_DEBUG = environ.get("DEBUG")
    SECRET_KEY = environ.get("SECRET_KEY")
    
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
    SQLALCHEMY_ECHO = environ.get("SQLALCHEMY_ECHO")
