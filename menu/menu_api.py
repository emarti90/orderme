# General Package Import
import re
from flask import json, jsonify, request, abort
from flask.views import MethodView
# User Package Import
from utilities.errorcodes import *
from utilities.filelogger import Log
from utilities.databaselayer import DatabaseLayer
from utilities.validator import validate_input
from utilities.schema import menu_schema
from user.decorators import user_required
from settings import database

# Class Menu API:
# This class acts as an interface to resolve HTTP petitions
class Menu_API(MethodView):
    decorators = [user_required]
    def __init__(self):
        lgr = Log('MENUAPI')
        self.log = lgr.getLog()

    def get(self, restaurant_id):
        try:
            self.log.info('Petition GET route INI')
            response = jsonify({}), 500
            menu = database.retrieveMenu(restaurant_id)
            self.log.debug(menu)
            if menu:
                self.log.info('Menu acquired succesfully')
                del menu['_id']
                self.log.debug(menu)
                response = jsonify(menu), 200
            else:
                error = {"code":err_ids}
                response = jsonify({"error":error}), 404
            self.log.info('Petition GET route END')
        except:
            error = {"code":err_unk}
            response = jsonify({"error":error}), 500
        finally:
            return response

    def post(self):
        try:
            self.log.info('Petition POST route INI')
            response = jsonify({}), 500
            menu = request.json
            self.log.debug(menu)
            if database.retrieveMenu(menu['restaurant_id']) is not None:
                error = {"code":err_aex}
                response = jsonify({"error":error}), 418
            else:
                requester = request.headers.get('X-USR-ID')
                self.log.debug(requester)
                user = database.retrieveUser(requester)
                acc = user.get('access')
                if (acc is not None) & (menu['restaurant_id'] in acc):                  
                    if validate_input(menu, menu_schema, self.log):
                        self.log.info('Creating Menu')
                        result = database.createMenu(menu)
                        if result:
                            response = jsonify({"result":"OK"}), 200
                        else:
                            error = {"error":err_dbf}
                            response = jsonify({"error":error}), 500
                    else:
                        error = {"code":err_frm}
                        response = jsonify({"error":error}), 400
                else:
                    error = {"code":err_nau}
                    response = jsonify({"error":error}), 403
            self.log. info('Petition POST route END')
        except:
            error = {"error":err_unk}
            resonse = jsonify({"error":error}), 500
        finally:
            return response

    def put(self, restaurant_id):
        try:
            self.log.info('Petition PUT route INI')
            response = jsonify({}), 500
            menu = request.json
            self.log.info(menu)
            m = database.retrieveMenu(restaurant_id)
            self.log.info(m)
            if database.retrieveMenu(restaurant_id):
                requester = request.headers.get('X-USR-ID')
                self.log.debug(requester)
                user = database.retrieveUser(requester)
                self.log.debug(user)
                acc = user.get('access')
                self.log.info(acc)
                if (acc is not None) & (restaurant_id in acc): 
                    if validate_input(menu, menu_schema, self.log):
                        if database.updateMenu(restaurant_id, menu):
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
            else:
                error = {"code":err_ids}
                response = jsonify({"error":error}), 404
            self.log.info('Petition PUT route END')
        except:
            error = {"error":err_unk}
            resonse = jsonify({"error":error}), 500
        finally:
            return response

    def delete(self, restaurant_id): 
        try:
            self.log.info('Petition DELETE route INI')
            response = jsonify({}), 500
            requester = request.headers.get('X-USR-ID')
            user = database.retrieveUser(requester)
            if restaurant_id in user.get('access'): 
                if database.deleteMenu(restaurant_id):
                    response = jsonify({"result":"OK"}), 200
                else:
                    error = {"code":err_dbf}
                    response = jsonify({"error":error}), 500
            else:
                error = {"code":err_nau}
                response = jsonify({"error":error}), 403
            self.log.info('Petition DELETE route END')
        except:
            error = {"error":err_unk}
            resonse = jsonify({"error":error}), 500
        finally:
            return response

