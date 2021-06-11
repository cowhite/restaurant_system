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


class Order:

    def __init__(self):
        self.db = connect_to_mongo()

    def update_order(self, order_id, order_status=None, table_id=None):

        if order_status is not None:
            attempted_update = self.db.orders.update_one({"order_id": order_id}, {"$set": {"order_status": order_status}})



        if table_id is not None:
            customer_table = self.db.customer_table.find_one({"_id": ObjectId(table_id), "is_available": True})
            if customer_table is not None:
                attempted_update = self.db.orders.update_one({"order_id": order_id}, {"$set": {"table_id": table_id}} )
                attempted_update = self.db.customer_table.update_one({"_id": ObjectId(table_id)}, {"$set": {"is_available": False}} )

            else:
                return {"status_code": 0, "message": "Selected table is not available, please choose another table"}
        return {"status_code": 1, "message": "Order data has been updated succesfully"}

    def get_orders_details(self, order_status):
        orders = parse_json(list(self.db.orders.find({"order_status": order_status})))
        print("@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(orders)
        print("@@@@@@@@@@@@@@@@@@@@")
        return {"status_code": 1, "message": "Success", "orders": orders}





    def calculate_item_price_after_discount(self, items_from_db, object_ids_with_quantity):
        total_price_before_discount = 0
        total_price_after_discount = 0
        items_info = []
        for item in items_from_db:
            item_info = {}
            item_price_before_discount = item['price']*object_ids_with_quantity[item['_id']]
            item_info['item_price'] = item_price_before_discount

            if item['discount_type'] == "percent":
                print("item@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                print(item)
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@item")
                item_price_after_discount = item_price_before_discount - item_price_before_discount*item['discount_value']/100
            elif item['discount_type'] == "flat":
                item_price_after_discount = item_price_before_discount - item['discount_value']


            item_info['_id'] = str(item['_id'])
            item_info['price'] = item['price']
            item_info['name'] = item['name']
            item_info['item_price'] = item_price_before_discount
            item_info['item_price_after_discount'] = item_price_after_discount
            item_info['discount_type'] = item['discount_type']
            item_info['discount_value'] = item['discount_value']
            item_info['quantity'] = object_ids_with_quantity[item['_id']]


            total_price_before_discount = total_price_before_discount + item_price_before_discount
            total_price_after_discount = total_price_after_discount + item_price_after_discount
            items_info.append(item_info)


        return items_info, total_price_before_discount, total_price_after_discount

    def calculate_item_price(self, items_from_db, object_ids_with_quantity):
        total_price = 0
        items_info = []
        for item in items_from_db:
            item_price = item['price']*object_ids_with_quantity[item['_id']]
            print("item_price")
            print(item_price)
            print("item_price")
            total_price = total_price + item_price
            item_info = {}
            item_info['_id'] = str(item['_id'])
            item_info['price'] = item['price']
            item_info['name'] = item['name']
            item_info['item_price'] = item_price

            items_info.append(item_info)
        print("items_info")
        print(items_info)
        print("items_info")
        return items_info, total_price





    def create_order(self, order_items, is_discount_available, customer_name, table_id, discount_level=None, discount_at_order_level=None, discount_type_at_order_level=None):
        total_price = 0
        order_items_with_object_id = []
        object_ids_with_quantity = {}
        order_info = []
        price_after_discount = 0
        print("table_id")
        print(table_id)
        items_info = []




        for order_item in order_items:
            order_items_with_object_id.append(ObjectId(order_item['_id']))
            print("order ids with object id")
            print(order_items_with_object_id)
            object_ids_with_quantity[ObjectId(order_item['_id'])] =  order_item['quantity']


        items_from_db = list(self.db.menu_items.find({"_id":{"$in": order_items_with_object_id }}))
        print("items_from_db")
        print(items_from_db)




        if is_discount_available and discount_level is not None and discount_level == "item_level":
            items_info, total_price, price_after_discount = self.calculate_item_price_after_discount(items_from_db=items_from_db, object_ids_with_quantity=object_ids_with_quantity)

        elif is_discount_available and discount_level is not None and discount_level == "order_level":
            items_info, total_price = self.calculate_item_price(items_from_db=items_from_db, object_ids_with_quantity=object_ids_with_quantity)
            if discount_type_at_order_level is not None and discount_type_at_order_level == "percent":
                price_after_discount = total_price - total_price*discount_at_order_level/100
            elif discount_type_at_order_level is not None and discount_type_at_order_level == "flat":
                price_after_discount = total_price - discount_at_order_level
        elif not is_discount_available:
            items_info, total_price = self.calculate_item_price(items_from_db=items_from_db, object_ids_with_quantity=object_ids_with_quantity)

            price_after_discount = total_price

        order_id = uuid.uuid4().hex

        attempted_entry_addition = self.db.orders.insert_one({"items_info": items_info, "total_price": total_price,
                                   "price_after_discount": price_after_discount, "customer_name": customer_name, "order_id": order_id, "order_status": "placed"})



        if attempted_entry_addition.inserted_id is not None:

            table = self.db.customer_table.find_one({"_id": ObjectId(table_id), "is_available": True})
            if table is None:
                return {"status_code": 1, "message": "Order has been placed succesfully, but the table you selected is not available, please select another table", "order_id": order_id}
            else:
                attempted_update = self.db.customer_table.update_one({"_id": ObjectId(table_id)}, {"$set": {"is_available": False}})



                return {"status_code": 1, "message": "Order has been placed succesfully", "order_id": order_id}
        return {"status_code": 0, "message": "Error Occured! Please contact support"}