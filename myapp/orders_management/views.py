from flask import jsonify, session, request
from .models import *
from myapp.decorator import json_required,form_required, query_params_required
import uuid
from myapp.utils.utils import myresponse


def update_order(order_id):
    request_data = request.json
    table_id = None
    order_status = None
    if "table_id" in request_data:
        table_id = request_data["table_id"]
    if "order_status" in request_data:
        order_status = request_data["order_status"]
    order = Order()
    response = order.update_order(order_id=order_id, order_status=order_status, table_id=table_id)
    return myresponse(response)
def get_orders_details(order_status):
    order = Order()
    response = order.get_orders_details(order_status=order_status)
    return myresponse(response)


@json_required(required_keys=["order_items", "customer_name", "table_id"])
def create_order():
    request_data = request.json
    order_items = request_data['order_items']
    customer_name = request_data['customer_name']
    table_id = request_data['table_id']
    discount_level = None
    discount_at_order_level = None
    discount_type_at_order_level = None
    is_discount_available = bool(request_data.get('is_discount_available', False))




    if is_discount_available:
        if "discount_level" in request_data:
            discount_level = request_data['discount_level']
        if discount_level == "order_level":
            if "discount_at_order_level" in request_data:
                discount_at_order_level = float(request_data["discount_at_order_level"])
            if "discount_type_at_order_level" in request_data:
                discount_type_at_order_level = request_data["discount_type_at_order_level"]


    order = Order()
    response = order.create_order(order_items=order_items, is_discount_available=is_discount_available,
     customer_name=customer_name, table_id=table_id, discount_level=discount_level, discount_at_order_level=discount_at_order_level,
      discount_type_at_order_level= discount_type_at_order_level)
    return myresponse(response)