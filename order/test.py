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

class OrderTest(unittest.TestCase):
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

    def generateItemOrder(self,item):
        itm = dict(item_id=item,
                  quantity=round(random.uniform(1,10),0),
                  item_amount=round(random.uniform(5, 25),2))
        return itm
    def generateOrder(self,rest, table):
        items = ["Aaaa", "Bbbb", "Cccc", "Dddd"]
        orders = list()
        tot = 0
        for i, itm in enumerate(items):
            orders.append(self.generateItemOrder(itm))

        order = dict(restaurant_id=rest, 
                    table_id=table,
                    waiter_id="Monica",
                    orders=orders,
                    total_amount=round(random.uniform(40,190),2))
        return order

    def authorizeUser(self, name, menu):
        usr = json.dumps(dict(user=name, password='isasecret', access=menu))
        manager.app.test_client().post('/users/', data=usr, content_type='application/json')
        rv = manager.app.test_client().post('/users/access/', data=usr, content_type='application/json')
        self.token = rv.get_json()['token']
        self.user = name
        return
    '''
    def test_createOrder(self):
        # Create an order
        # Obtain authorization
        self.authorizeUser("crtord", "ElSitio")
        # Generate random order
        data = json.dumps(self.generateOrder("ElSitio","001"))
        # POST request
        rv = manager.app.test_client().post('/orders/', data=data, content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        self.assertEqual(rv.status_code,200,"ORDERAPI - Create order FAIL")
    
    def test_retrieveOrder(self):
        # Retrieve an order
        # Obtain authorization
        self.authorizeUser("getord", "ElSitio")
        # Generate an order and store it
        data = json.dumps(self.generateOrder("ElSitio","002"))
        manager.app.test_client().post('/orders/', data=data, content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        # GET request
        rv = manager.app.test_client().get('/orders/ElSitio/002', content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        self.assertEqual(rv.status_code, 200, "ORDERAPI - Retreive order FAIL")
    
    def test_addtoOrder(self):
        # Update an order by adding an item
        # Obtain authorization
        self.authorizeUser("uptord", "ElSitio")
        # Generate and order and store it
        order = self.generateOrder("ElSitio","003")
        data = json.dumps(order)
        manager.app.test_client().post('/orders/', data=data, content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        # Modify order
        order['orders'].append(self.generateItemOrder("X"))
        data = json.dumps(order)
        # PUT request
        rv = manager.app.test_client().put('/orders/ElSitio/003', data=data, content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        self.assertEqual(rv.status_code, 200, 'Test add item to order FAIL')

    def test_removefromOrder(self):
        # Uodate an order by removing an item
        # Obtain authorization
        self.authorizeUser("updord","ElSitio")
        # Generate Order
        order = self.generateOrder("ElSitio","004")
        data = json.dumps(order)
        manager.app.test_client().post('/orders/', data=data, content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        # Modify order
        del order['orders'][0]
        data = json.dumps(order)
        rv = manager.app.test_client().put('/orders/ElSitio/004', data=data, content_type='application/json', headers={'X-USR-ID':self.user, 'X-USR-TK':self.token})
        self.assertEqual(rv.status_code, 200, 'Test remove item from order FAIL')
    '''