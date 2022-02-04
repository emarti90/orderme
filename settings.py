import logging

from flask_pymongo.wrappers import MongoClient

SECRET_KEY = 'order-it-magic-word'

APP_DEBUG = True
APP_HOST = 'localhost'
APP_PORT = 5000

MONGO_URI = 'mongodb://localhost/orderme'

LOGLEVEL = logging.DEBUG

MONGODB_HOST = 'mongodb' # use 'mongodb' if using Docker

from utilities.databaselayer import DatabaseLayer

database = DatabaseLayer(MongoClient(host=MONGO_URI))