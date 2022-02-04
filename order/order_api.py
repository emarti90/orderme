# General Package Import
from flask import jsonify, request, abort
from flask.views import MethodView
# User Package Import
from utilities.errorcodes import *
from utilities.filelogger import Log
from utilities.databaselayer import DatabaseLayer
from utilities.validator import validate_input
from utilities.schema import order_schema, checkout_schema
from user.decorators import user_required
from settings import database

# Class Order API:
# This class acts as an interface to resolve HTTP petitions
class Order_API(MethodView):
    decorators = [user_required]
    def __init__(self):
        lgr = Log('ORDERAPI')
        self.log = lgr.getLog()

    def checkAccesibility(self, restaurant_id, table_id, user_id):
        try:
            self.log.info('checkAccesibility INI')
            result = False
            user = database.retrieveUser(user_id)
            role = user.get('role')
            access = user.get('access')
            if role == "OWNER":
                if restaurant_id in access:
                    result = True
            else:
                if (restaurant_id in access) and (table_id in access):
                    result = True
            self.log.info('checkAccesibility END')
        except:
            result = False
        finally:
            return result

    def addToTab(self, restaurant_id, table_id, order):
        tableOrd = database.retrieveTableTab(restaurant_id, table_id)
        tableTab = tableOrd['tab']
        for ord in order:
            idx = next((i for i, it in tableTab if it['item_id'] == ord['item_id']),None)
            if idx is not None:
                itm = tableTab[idx]
                itm['quantity'] = itm['quantity'] + ord['quantity']
                tableTab[idx] = itm
            else:
                tableTab.append(ord)
        return tableTab

    def get(self, restaurant_id, table_id):
        try:
            self.log.info('Petition GET route INI')
            response = jsonify({}), 500
            tab = database.retrieveTableTab(restaurant_id, table_id)
            requester = request.headers.get('X-USR-ID')
            if self.checkAccesibility(restaurant_id, table_id, requester):
                if tab:
                    response = jsonify(tab), 200
                else:
                    error = {"code":err_ids}
                    response = jsonify({"error":error}), 404
            else:
                error = {"code":err_nau}
                response = jsonify({"error":error}), 403
            self.log.info('Petition GET route END')
        except:
            error = {"code":err_unk}
            response = jsonify({"error":error}), 500
        finally:    
            return response

    def post(self):
        try:
            self.log.info('Petition POST INI')
            response = jsonify({}), 500
            order = request.json
            requester = request.headers.get('X-USR-ID')
            restaurant = order.get('restaurant_id')
            table = order.get('table_id')
            if self.checkAccesibility(restaurant,table, requester):
                if validate_input(order, order_schema, self.log):
                    result = database.createTableOrder(order)
                    if result:
                        tab = self.addToTab(restaurant, table, order['orders'])
                        result = database.updateTableTab(restaurant, table, tab)  
                    if result:
                        response = jsonify({"result":"OK"}), 200
                    else:
                        error = {"code":err_dbf}
                        response = jsonify({"error":error}), 500
                else:
                    error = {"code":err_frm}
                    response = jsonify({"error":error}), 400
            else:
                error = {"code":err_nau}
                response = jsonify({"error":error}), 403
            self.log.info('Petition POST END')
        except:
            error = {"code":err_unk}
            response = jsonify({"error":error}), 500
        finally:
            return response

    def put(self, restaurant_id, table_id):
        try:
            self.log.info('Petition PUT route INI')
            response = jsonify({}), 500
            order = request.json
            requester = request.headers.get('X-USR-ID')
            if self.checkAccesibility(restaurant_id, table_id, requester):
                if database.retrieveTableOrder(restaurant_id,table_id):
                    if validate_input(order, checkout_schema, self.log):
                        if database.updateTableTab(restaurant_id, table_id, order):
                            response = jsonify({"result":"OK"}), 200
                        else:
                            error = {"code":err_dbf}
                            response = jsonify({"error":error}), 500
                    else:
                        error = {"code":err_frm}
                        response = jsonify({"error":error}), 400
                else:
                    error = {"code":err_ids}
                    response = jsonify({"error":error}), 404
            else:
                error = {"code":err_nau}
                response = jsonify({"error":error}), 403
            self.log.info('Petition PUT route END')
        except:
            error = {"code":err_unk}
            response = jsonify({"error":error}), 500
        finally:
            return response

