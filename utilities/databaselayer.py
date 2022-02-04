# Import General Packages
import json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import  ASCENDING, DESCENDING, ReturnDocument
# Import User Packages
from utilities.filelogger import Log

# Class DatabaseLayer

class DatabaseLayer:
    def __init__(self, database):
        self.database = database
        lgr = Log('DATABASELAYER')
        self.log = lgr.getLog()

    # DEF: check database connection
    # PARAM: None
    # RETURN: True if OK / False otherwise
    def checkStatus(self):
        self.log.info('checkStatus() INI')
        result = False
        if self.database.db.users.find_one() is not None:
            result = True
        self.log.info('checkStatus() END > database ready')
        return result

# Menu operations

    # DEF: create a menu
    # PARAM:  menu - the menu as a list of menu items in JSON format
    # RETURN: True if OK / False Otherwise
    def createMenu(self, menu):
        self.log.info('createMenu() INI')
        result = False
        dbres = self.database.db.menus.insert_one(menu)
        if dbres.inserted_id:
            result = True
        self.log.info('createMenu() END')
        return result

    # DEF: delete a menu
    # PARAM: menu_id - id of the menu to be deleteds
    # RETURN: True if OK / False Otherwise
    def deleteMenu(self, menu_id):
        self.log.info('deleteMenu() INI')
        result = False
        dbres = self.database.db.menus.delete_one({'restaurant_id':menu_id})
        self.log.info(dbres)
        if dbres.deleted_count > 0:
            result = True
        self.log.info('deleteMenu() END')
        return result
    
    # DEF: update a menu
    # PARAM: menu_id - id of the menu to be updated
    #        menu    - the menu info in the proper JSON format
    # RETURN: True if OK / False Otherwise
    def updateMenu(self, menu_id, menu):
        self.log.info('updateMenu() INI')
        result = False
        dbres = self.database.db.menus.replace_one({'restaurant_id':menu_id}, menu, upsert=True)
        if dbres.modified_count > 0:
            result = True
        self.log.info('updateMenu() END')
        return result

    # DEF: retrieve a menu
    # PARAM: menu_id - id of the menu to be retrieved
    # RETURN: Menu in JSON format if OK / None Otherwise
    def retrieveMenu(self, restaurant_id):
        self.log.info('retrieveMenu() INI')
        result = None
        self.log.debug('retrieveMenu() with id: ' + restaurant_id)
        dbres = self.database.db.menus.find_one({'restaurant_id':restaurant_id})
        
        if dbres != None:
            result = dbres
        self.log.info('retrieveMenu() END')
        return result

# Order operations

    # DEF: create an order in the database
    # PARAM: the order to be created in JSON format
    # RETURN: True if OK / False otherwise
    def createTableOrder(self, order):
        self.log.info('createOrder() INI')
        result = False
        dbres = self.database.db.orders.insert_one(order)
        if dbres.inserted_id is not None:
            result = True
        self.log.info('createOrder() END')
        return result

    # DEF: update table order
    # PARAM: table_id - table to be updated
    #        table - the table oreder in the proper JSON format
    # RETURN: True if OK / False otherwise
    def updateTableOrder(self, restaurant_id, table_id, order):
        self.log.info('updateTableOrder() INI')
        result = False
        dbres = self.database.db.orders.replace_one({'restaurant_id':restaurant_id,'table_id':table_id}, order, upsert=True)
        self.log.debug(dbres)
        if dbres.modified_count > 0:
            result = True
        self.log.info('updateTableOrder() END')
        return result

    # DEF: retrieve a table order
    # PARAM: table_id - table to be retrieved
    # RETURN: Table in JSON format / None otherwise
    def retrieveTableOrder(self, restaurant_id, table_id):
        self.log.info('retrieveTableOrder() INI')
        result = None
        dbres = self.database.db.orders.find_one({'restaurant_id':restaurant_id,'table_id':table_id})
        if dbres != None:
            result = dbres
        self.log.info('retrieveTableOrder() END')
        return result

    # DEF: update table tab
    # PARAM: table_id - table to be updated
    #        table - the table oreder in the proper JSON format
    # RETURN: True if OK / False otherwise
    def updateTableTab(self, restaurant_id, table_id, order):
        self.log.info('updateTableOrder() INI')
        result = False
        dbres = self.database.db.orders.update_one({'restaurant_id':restaurant_id,'table_id':table_id}, {'$set':order}, upsert=True)
        self.log.debug(dbres)
        if dbres.modified_count > 0:
            result = True
        self.log.info('updateTableOrder() END')
        return result

    # DEF: retrieve a table tab
    # PARAM: table_id - table to be retrieved
    # RETURN: Table in JSON format / None otherwise
    def retrieveTableTab(self, restaurant_id, table_id):
        self.log.info('retrieveTableOrder() INI')
        result = None
        dbres = self.database.db.orders.find_one({'restaurant_id':restaurant_id,'table_id':table_id}, projection={'_id':False,'orders':False})
        if dbres != None:
            result = dbres
        self.log.info('retrieveTableOrder() END')
        return result

# User operations

    # DEF: create a User
    # PARAM: user - the user in JSON format to be created
    # RETURN: True if Ok / False Otherwise
    def createUser(self, user):
        self.log.info('createUser() INI')
        result = False
        dbres = self.database.db.users.insert_one(user)
        self.log.debug(dbres)
        if dbres != None:
            result = True
        self.log.info('createUser() END')
        return result

    # DEF: delete a user
    # PARAM: user_id - the user to be deleted
    # RETURN: True if OK / False Otherwise
    def deleteUser(self, user_id):
        self.log.info('deleteUser() INI')
        result = None
        dbres = self.database.db.users.delete_one({'user':user_id})
        if dbres != None:
            result = dbres
        self.log.info('deleteUser() END')
        return result

    # DEF: update a user (token & expiration ONLY)
    # PARAM: user - the user in JSON format (access_schema)
    # RETURN: True if OK / False Otherwise
    def updateUser(self, user):
        self.log.info('updateUser() INI')
        result = False
        dbusr = self.database.db.users.find_one({'user':user['user']})
        if dbusr is not None:
            dbusr['token'] = user.get('token')
            dbusr['expires'] = user.get('expires')
            dbres = self.database.db.users.find_one_and_replace({'user':user['user']}, user, return_document=ReturnDocument.AFTER)
            if dbres is not None:
                result = True
        self.log.info('updateUser() END')
        return result

    # DEF: retrieve a user
    # PARAM: user_id - the user id to be retrieved
    # RETURN: user in JSON format if OK / None Otherwise
    def retrieveUser(self, user_id):
        self.log.info('retrieveUser() INI')
        result = None
        dbres = self.database.db.users.find_one({'user':user_id})
        self.log.debug(dbres)
        if dbres != None:
            result = dbres
        self.log.info('retrieveUser() END')
        return result

'''
# Menu Item operations

    # DEF: insert an item
    # PARAM: item - item in JSON format
    # RETURN: True if OK / None Otherwise
    def createMenuItem(self, menu_id, item):
        self.log.info('createMenuItem() INI')
        result = None
        dbres = self.database.db.menus.insert_one(item)
        if dbres.inserted_id != None:
            result = True
        self.log.info('createMenuItem() END')
        return result

    # DEF: delete an item
    # PARAM: item_id - id of the menu to be deleted
    # RETURN: True if OK / False Otherwise
    def deleteMenuItem(self, item_id):
        self.log.info('deleteMenuItem() INI')
        result = None
        dbres = self.database.db.menus.find_one_and_delete({'restaurant_id':menu_id,'item_id':item_id})
        if dbres.deleted_count > 0:
            result = True
        self.log.info('createMenuItem() END')
        return result

    # DEF: update an item
    # PARAM: item_id - id of the menu to be deleted
    # RETURN: True if OK / False Otherwise
    def updateMenuItem(self, item_id, item):
        self.log.info('updateMenuItem() INI')
        result = None
        dbres = self.database.db.menus.find_one_and_replace({'item_id':item_id}, item, return_document = ReturnDocument.AFTER)
        if dbres.modified_count != None:
            result = True
        self.log.info('updateMenuItem() END')
        return result
'''