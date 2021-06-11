from myapp.mongoconnect import connect_to_mongo
from myapp.utils.utils import (
    myresponse, parse_json
)
from flask import json

import uuid
from .constants import *
import bson
import os
from bson import ObjectId
import datetime
import pymongo


class MenuItems:

    def __init__(self):
        self.db = connect_to_mongo()

    def get_menu_details(self, limit=100, offset=0):
        menu_items = list(self.db.menu_items.find({}).skip(offset).limit(limit))
        menu_items = parse_json(menu_items)
        return {"data": menu_items, "status_code": 1, "message": "Success"}

    def edit_menu_item(self, menu_item, id):
        self.db.menu_items.update_one(
            {"_id": ObjectId(id)},
            {"$set": menu_item}
        )
        return {"status_code": 1, "message": "Menu has been updated succesfully"}

    def delete_menu_item(self, _id):
        try:
            print(_id)
            attempted_deletion = self.db.menu_items.delete_one({"_id": ObjectId(_id)})
            if attempted_deletion.deleted_count == 1:
                return {"status_code": 1, "message": "Menu item deleted succesfully"}
            return {"status_code": 0, "message": "Deletion Failed! Please contact support"}
        except bson.errors.InvalidId:
            return {"status_code": 0, "message": "Invalid menu_item. Please provide a valid one"}


    def add_menu_items(self, menu_items_list):
        errors = []
        items_to_be_added = []
        response = None

        if menu_items_list is not None:
            for menu_item in menu_items_list:
                i = 0
                error = {}
                name = None
                price = None
                discount_type = None
                discount_value = None
                if "name" not in menu_item:
                    error['name'] = "name not given for the %sst item in the list" % i
                if "price" not in menu_item:
                    error['price'] = "price not given for the %sst item in the list" % i
                if "discount_type" not in menu_item:
                    error['discount_type'] = "discount_type not given for the %sst item in the list" % i
                if "discount_type" not in menu_item:
                    error['discount_value'] = "discount_value not given for the %sst item in the list" % i
                if error:
                    errors.append(error)
                    continue






                name = menu_item['name']
                price = float(menu_item['price'])
                discount_type = menu_item['discount_type']
                discount_value = float(menu_item['discount_value'])
                item_to_be_added = {"name": name, "price": price, "discount_type": discount_type, "discount_value": discount_value }
                items_to_be_added.append(item_to_be_added)






        if errors:
            response = {"status_code": 0, "message": "Error adding the menu items. Please contact support", "error_data": errors}

            return response
        attempted_insertion = None
        try:
            attempted_insertion = self.db.menu_items.insert_many(items_to_be_added, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            print("duplicate found, do nothing")

        '''if attempted_insertion is not None and len(attempted_insertion.inserted_ids) >=1:'''
        response =  {"status_code": 1, "message": "Menu items have been added succesfully"}
        '''else:
            response =  {"status_code": 0, "message": "Error adding the menu items. Please contact support"}'''




        return response




