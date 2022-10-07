from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # using this for the database
from os import path
from flask_login import LoginManager

db = SQLAlchemy()  # initializes the database
DB_NAME = "database.db"  # variable and name can be anything


def create_app():
    # initializes app, __name__ represents the name of the file that was ran
    app = Flask(__name__)
    # encrypt cookies/session data related to website, can be anything
    app.config['SECRET_KEY'] = 'random_secret'
    # this tells Flask that this is where my SQLAlchemy db is stored at this location
    # here that's 'my_app'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # takes the db i defined and tells it that i'm using this app with it
    db.init_app(app)

    # importing blueprints
    from .views import views
    from .auth import auth

    # registers blueprints to the app
    # url_prefix explains the prefix required to access the urls in each file
    # here '/' means no prefix
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

# importing models so that we make sure that they are initialized before db is created by running that file first
    from .models import User, Event

    create_database(app)

# LoginManager manages login functions
# has to be put in after the models and creating db
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
# telling flask how we're loading the user and which one we're looking for

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app  # creates the app

# determines whether this db has been created or not
# if it doesn't exist, it creates it with this app


def create_database(app):
    if not path.exists('my_app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
