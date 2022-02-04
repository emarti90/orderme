# General Packages Import
from flask import Blueprint
# User Pacakages Import
from order.order_api import Order_API

order_app = Blueprint('order_app', __name__)

order_view = Order_API.as_view('order_api')

order_app.add_url_rule('/orders/', view_func = order_view, methods = ['POST',])
order_app.add_url_rule('/orders/<restaurant_id>/<table_id>', view_func = order_view, methods = ['PUT', 'GET',])