from flask import jsonify, session, request
from .models import *
from myapp.decorator import json_required,form_required, query_params_required, put_json_required
import uuid
from myapp.utils.utils import myresponse
import json


@json_required(required_keys=["menu_items_list"])
def add_menu_items():
    request_data = request.json

    menu_items_list= request_data['menu_items_list']
    menu_items = MenuItems()
    response = menu_items.add_menu_items(menu_items_list=menu_items_list)
    return myresponse(response)

@put_json_required(required_keys=["menu_item", "_id"])
def update_menu_item():
    request_data = request.json
    menu_item = request_data['menu_item']
    _id = request_data['_id']
    menu_items = MenuItems()
    response = menu_items.edit_menu_item(menu_item=menu_item, id=_id)
    return myresponse(response)


def delete_menu_item(_id):

    menu_items = MenuItems()
    response = menu_items.delete_menu_item(_id=_id)
    return myresponse(response)


