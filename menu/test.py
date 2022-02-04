# General Packages
import unittest
import json
import random
from pymongo import MongoClient
# User Packages
import manager, settings
from application import create_app as create_app_base
from application import config_app as config_app_base
from utilities.databaselayer import DatabaseLayer

class MenuTest(unittest.TestCase):
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

    def generateItem(self, item):
        allerg = ["gluten" ,"crustacean","egg","fish","peanut",
                  "soybean","milk","nut","celery","mustard",
                  "sesame" ,"sulph","lupin","molluc","none"]
        catego = ["appetizers", "main course", "dessert", "drinks"]

        itm = dict(item_id=item, 
                 allergens=random.sample(allerg,random.randint(1,5)), 
                 category=random.choice(catego), 
                 prize=round(random.uniform(0,10),2))
        return itm
    
    def generateMenu(self, restaurant):
        items = ["myDishA","myDishE","myDishI","myDishO","myDishU"]
        mitems = list()
        for itm in items:
            mitems.append(self.generateItem(itm))
        menu = dict(restaurant_id = restaurant, menu_items=mitems)
        return menu
    
    def authorizeUser(self, name, menu):
        usr = json.dumps(dict(user=name, password='isasecret', access=menu))
        manager.app.test_client().post('/users/', data=usr, content_type='application/json')
        rv = manager.app.test_client().post('/users/access/', data=usr, content_type='application/json')
        self.token = rv.get_json()['token']
        self.user = name
        return
    
    def test_createMenu(self):
        # Create Basic Menu
        # Authorize temporary user
        self.authorizeUser('crtmenu', 'myDinner')
        # Generate Menu
        data = json.dumps(self.generateMenu("myDinner"))
        # POST request
        rv = manager.app.test_client().post('/menu/', data=data, content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        self.assertEqual(rv.status_code, 200, 'MENU_API - Create menu FAILED')
    
    def test_retrieveMenu(self):
        # Retrieve an existing menu
        # Authorize temporary user
        self.authorizeUser('getmenu', 'MonMenu')
        # Generate Menu and insert into DB
        data = json.dumps(self.generateMenu('MonMenu'))
        manager.app.test_client().post('/menu/', data=data, content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        # GET request
        rv = manager.app.test_client().get('/menu/MonMenu', content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        self.assertEqual(rv.status_code, 200, 'MENUAPI - Retrieve menu FAILED')
    
    def test_updateMenu(self):
        # Update an existing Menu
        # Authorize temporary user
        self.authorizeUser('putmenu', 'TuMenu')
        # Generate Menu
        menu = self.generateMenu("TuMenu")
        data = json.dumps(menu)
        manager.app.test_client().post('/menu/', data=data, content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        # PUT request
        menu['menu_items'].append(self.generateItem('myDishXYZ'))
        data = json.dumps(menu)
        rv = manager.app.test_client().put('/menu/TuMenu', data=data, content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        self.assertEqual(rv.status_code, 200, 'MENUAPI - Update menu FAILED')

    def test_deleteMenu(self):
        # Delete an existing Menu
        # Authorize temporary user
        self.authorizeUser('delmenu', 'IlMioMenu')
        # Generate Menu
        menu = self.generateMenu("IlMioMenu")
        data = json.dumps(menu)
        manager.app.test_client().post('/menu/', data=data, content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        # DELETE request
        rv = manager.app.test_client().delete('/menu/IlMioMenu', content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        self.assertEqual(rv.status_code, 200, 'MENUAPI - Delete menu FAILED')





