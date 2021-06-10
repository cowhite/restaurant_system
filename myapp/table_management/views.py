from flask import jsonify, session, request
from .models import *
from myapp.decorator import json_required,form_required, query_params_required
import uuid
from myapp.utils.utils import myresponse

def add_table():
    request_data = request.json
    seat_count = request_data['seat_count']
    is_available = bool(request_data['is_available'])
    customer_table = CustomerTable()
    response = customer_table.add_table(seat_count=seat_count, is_available=is_available)
    return myresponse(response)

def delete_table(_id):
    customer_table = CustomerTable()
    response = customer_table.delete_table(_id=_id)
    return myresponse(response)

def update_table(_id):
    customer_table = CustomerTable()
    request_data = request.json
    table_number = None
    is_available = None

    if "is_available" in request_data:
        is_available = request_data["is_available"]

    if "table_number" in request_data:
        is_available = None
        table_number = request_data["table_number"]


    response = customer_table.update_table(_id=_id, is_available=is_available, table_number=table_number)
    return myresponse(response)



