# General Packages
import unittest
import json
from pymongo import MongoClient
# User Packages
import manager, settings
from application import create_app as create_app_base
from application import config_app as config_app_base
from utilities.databaselayer import DatabaseLayer

class UserTest(unittest.TestCase):
    def create_app(self):
        settings.MONGO_URI = 'mongodb://localhost/tests'
        settings.APP_DEBUG = True
        return create_app_base()

    def setUp(self):
        manager.app = self.create_app()
        settings.database = DatabaseLayer(MongoClient(settings.MONGO_URI))
        config_app_base(manager.app)

    def tearDown(self):
        settings.database.database.drop_database('tests')

    def test_createUser(self):
        # Basic user registration
        data = json.dumps(dict(user = 'crttestusr', password = 'secretest'))
        rv = manager.app.test_client().post('/users/', data=data, content_type='application/json')
        self.assertEqual(rv.status_code, 200, 'USER_API - Create new user FAIL')

    def test_createUserNoPass(self):
        # Attempt to create a user without password
        data = json.dumps(dict(user = 'testusrnp'))
        rv = manager.app.test_client().post('/users/', data=data, content_type='application/json')
        self.assertEqual(rv.status_code, 400, 'USER_API - Create user with no pass FAIL')

    def test_createUserNoName(self):
        # Attempt to create a user without password
        data = json.dumps(dict( password = 'secrettestnn'))
        rv = manager.app.test_client().post('/users/', data=data, content_type='application/json')
        self.assertEqual(rv.status_code, 400, 'USER_API - Create user with no name FAIL')

    def test_authorizeUser(self):
        # Authorise existing user
        data = json.dumps(dict(user = 'auttestusr', password = 'secretest'))
        manager.app.test_client().post('/users/', data=data, content_type='application/json')
        rv = manager.app.test_client().post('/users/access/', data=data, content_type='application/json')
        self.assertEqual(rv.status_code, 200, 'USER_API - Existing user authorization FAIL')


