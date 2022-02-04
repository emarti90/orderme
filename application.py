# General Package
from flask import Flask
from flask_pymongo import PyMongo
# User Packages
from settings import MONGO_URI

def create_app(**config_overrides):
    # Import All
    import packages
    # Create Flask Application
    app = Flask(__name__)
    # App Configuration
    app.config['MONGO_URI'] = MONGO_URI
    return app

def config_app(app):
    # import blueprints
    from menu.views import menu_app
    from order.views import order_app
    from user.views import user_app


    # register blueprints
    app.register_blueprint(menu_app)
    app.register_blueprint(order_app)
    app.register_blueprint(user_app)

    return

def create_db(app):
    # Create Database
    db = PyMongo(app)
    return db