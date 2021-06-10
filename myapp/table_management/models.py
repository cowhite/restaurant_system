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


class CustomerTable:

    def __init__(self):
        self.db = connect_to_mongo()

    def add_table(self, seat_count, is_available):
        table_number = 1
        customer_table = self.db.customer_table.find_one(sort=[( '_id', pymongo.DESCENDING )])
        if customer_table is not None:
            table_number = customer_table['table_number']
            table_number = table_number + 1
        attempted_entry_addition = self.db.customer_table.insert_one({"table_number": table_number, "seat_count":seat_count, "is_available": is_available})
        if attempted_entry_addition.inserted_id is not None:



            return {"status_code": 1, "message": "New Table Entry added succesfully"}
        return {"status_code": 0, "message": "Error Occured! Please contact support"}

    def delete_table(self, _id):

        try:
            attempted_entry_deletion = self.db.customer_table.delete_one({"_id": ObjectId(_id)})
            if attempted_entry_deletion.deleted_count == 1:
                return {"status_code": 1, "message": "Table deleted succesfully"}
            return {"status_code": 0, "message": "Deletion Failed! Please contact support"}
        except bson.errors.InvalidId:
            return {"status_code": 0, "message": "Invalid Table. Please provide a valid one"}

    def update_table(self, _id, is_available=None, table_number=None):
        attempted_update = None
        try:
            if is_available is not None:
                attempted_update = self.db.customer_table.update_one( {"_id": ObjectId(_id)} , {"$set":  {"is_available": is_available}})
            elif table_number is not None:
                try:
                    attempted_update = self.db.customer_table.update_one( {"_id": ObjectId(_id)} , {"$set":  {"table_number": table_number}})
                except pymongo.errors.DuplicateKeyError as e:
                    return {"status_code": 1, "message": "Table with this table_number already exists"}
            if attempted_update.modified_count == 1:
                return {"status_code": 1, "message": "Table data changed succesfully"}
            return {"status_code": 0, "message": "Looks like table data changed already. If you need further assistance, please contact support"}
        except bson.errors.InvalidId:
            return {"status_code": 0, "message": "Invalid Table. Please provide a valid one"}






