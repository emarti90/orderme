# General Packages Import
from flask import Blueprint
# User Pacakages Import
from menu.menu_api import Menu_API

menu_app = Blueprint('menu_app',__name__)

menu_view = Menu_API.as_view('menu_api')

menu_app.add_url_rule('/menu/', view_func = menu_view, methods = ['POST',])
menu_app.add_url_rule('/menu/<restaurant_id>', view_func = menu_view, methods = ['GET', 'PUT', 'DELETE',])