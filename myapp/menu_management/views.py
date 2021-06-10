from flask import jsonify, session, request
from .models import *
from myapp.decorator import json_required,form_required, query_params_required
import uuid
from myapp.utils.utils import myresponse
import json

def get_menu_details():
    query_params = request.args
    limit = int(query_params.get("limit", 100))
    offset = int(query_params.get("offset", 0))
    menu_tems = MenuItems()
    menu_details = menu_items.get_menu_details(limit=limit, offset=offset)
    return myresponse(menu_details)

def add_menu_items():
    request_data = request.json
    print(request_data['menu_items_list'])
    menu_items_list= request_data['menu_items_list']
    menu_items = MenuItems()
    response = menu_items.add_menu_items(menu_items_list=menu_items_list)
    return myresponse(response)

def update_menu_item():
    request_data = request.json
    menu_item = request_data['menu_item']
    _id = request_data['_id']
    menu_items = MenuItems()
    response = menu_items.edit_menu_item(menu_item=menu_item, id=_id)
    return myresponse(response)



