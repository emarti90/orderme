# General Packages Import
from flask import Blueprint
# User Pacakages Import
from user.user_api import Access_API, User_API

user_app = Blueprint('user_app', __name__)

user_view = User_API.as_view('user_api')
user_app.add_url_rule('/users/', view_func = user_view, methods = ['POST',])

access_view = Access_API.as_view('access_api')
user_app.add_url_rule('/users/access/', view_func = access_view, methods = ['POST',])