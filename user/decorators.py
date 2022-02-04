# General Package Import
import datetime
from functools import wraps
from flask import json, request, jsonify
# User Package Import
from utilities.filelogger import Log
from utilities.databaselayer import DatabaseLayer
from utilities.errorcodes import *
from settings import database


def user_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        lgr = Log('DECORATOR')
        log = lgr.getLog()
        log.info('Decorated function INI')
        user_id = request.headers.get('X-USR-ID')
        user_token = request.headers.get('X-USR-TK')
        if user_id is None or user_token is None:
            return jsonify({}), 403
        user = database.retrieveUser(user_id)
        log.debug(user)
        if not user:
            return jsonify({}), 403
        log.debug('Check user legibility')
        if user['token'] is None:
            return jsonify({}), 403
        if user['token'] != user_token:
            return jsonify({}), 403
        if user['expires'] < datetime.datetime.utcnow():
            error = jsonify({"code":err_tkn})
            return jsonify({"error":error}), 403
        log.info('Decorated function END')
        return f(*args,**kwargs)
    return decorated_function
