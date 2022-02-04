# General Package Import
import json
import uuid
import bcrypt
from datetime import datetime, timedelta
from flask import jsonify, request, abort
from flask.views import MethodView
import pymongo

# User Package Import
from utilities.errorcodes import *
from utilities.filelogger import Log
from utilities.databaselayer import DatabaseLayer
from utilities.validator import validate_input
from utilities.schema import user_schema
from utilities.schema import access_schema
from settings import database


# Class User API:
# This class resolve sing-in petitions for new users
class User_API(MethodView):
    def __init__(self):
        lgr = Log('USERAPI')
        self.log = lgr.getLog()

    def post(self):
        try:
            self.log.info("Petition POST route INI")
            response = jsonify({}), 500
            data = request.json
            if validate_input(data, user_schema, self.log):
                exist_user = database.retrieveUser(data['user'])
                self.log.debug(exist_user)
                if not exist_user: # Create the credentials
                    hashedpw = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt())
                    data['password'] = hashedpw
                    database.createUser(data)
                    self.log.debug(data)
                    response = jsonify({"result":"OK"})
                else: 
                    error = {"code":err_aex}
                    response = jsonify({"error":error}), 400
            else:
                error = {"code":err_ids}
                response = jsonify({"error":error}), 400
                self.log.info("Petition POST route END")
        except:
            self.log.info('Unkown error')
            error = {"code":err_unk}
            response = jsonify({"error":error}), 500
        finally:
            return response
        

# Class Access API
# This class resolve log-in Token based petitions for existing users
class Access_API(MethodView):
    def __init__(self):
        self.lgr = Log('ACCESSAPI')
        self.log = self.lgr.getLog()
    
    def post(self):
        try:
            self.log.info('Petition POST route INI')
            response = jsonify({}), 500
            data = request.json
            if validate_input(data, access_schema, self.log):
                exist_user = database.retrieveUser(data['user'])
                self.log.debug(exist_user)
                if exist_user: # Generate Token
                    if bcrypt.hashpw(data['password'].encode('UTF-8'), exist_user['password']) == exist_user['password']:
                        self.log.info('Generating token')
                        token = str(uuid.uuid4())
                        now = datetime.utcnow().replace(second=0, microsecond=0)
                        expires = now + timedelta(days=30)
                        exist_user['token'] = token
                        exist_user['expires'] = expires
                        database.updateUser(exist_user)
                        expires_3339 = expires.isoformat('T') + 'Z'
                        response = jsonify({'token':token,'expires':expires_3339})
                        self.log.info(response)
                    else:
                        self.log.info('Incorrect password')
                        error = {"code":err_pwd}
                        response = jsonify({"error":error}), 403
                else:
                    self.log.info('User does not exist')
                    error = {"code":err_pwd}
                    response = jsonify({"error":error}), 403
            else:
                self.log.info('Invalid input')
                error = {"code":err_ids}
                response = jsonify({"error":error}), 400
            self.log.info('Petittion POST route END')
        except:
            self.log.info('Unkown error')
            error = {"code":err_unk}
            response = jsonify({"error":error}), 500
        finally:
            return response
            
        
        
