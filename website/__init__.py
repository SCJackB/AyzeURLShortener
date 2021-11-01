from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sqlalchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    # define 'app' as a Flask app
    app = Flask(__name__)
    # generate the flask secret key
    app.config["SECRET_KEY"] = os.urandom(12).hex()
    # Tell flask where the database is
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    # initiallise the database with the flask app
    db.init_app(app)

    # import the views and auth blueprints from the 'website' package
    from .views import views
    from .auth import auth

    # register url prefixs
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # import the database classes
    from .models import User, urls

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)

    # run app
    return app


def create_database(app):
    # if the database doesnt exist
    if not path.exists("website/" + DB_NAME):
        # create the database
        db.create_all(app=app)
