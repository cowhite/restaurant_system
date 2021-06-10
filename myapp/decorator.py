from flask import flash, json
from flask import redirect
from flask import session
from flask import url_for
from flask import request, jsonify
from functools import wraps

import inspect


def check_for_required_fields(data, required_keys):
    error_response = {"errors": {}}
    '''if "txn_source_id" in data:
        if len(data['txn_source_id']) > 35:
            error_response["error"] = True
            error_response['errors']["txn_source_id"] = "txn_source_id maximum length is 35"'''

    for key in required_keys:
        if key not in data or data[key] == "" or data[key] == None or data[key] == "null":
            error_response['error'] = True
            error_response['errors'][key] = "This field is required"
        elif key in data and data[key] != None and type(data[key]) != bool and str(data[key]).strip() == "":
            error_response['error'] = True
            error_response['errors'][key] = "This field is required"

    return error_response





def json_required(required_keys=[]):
    def decorator(f):
        @wraps(f)
        def wrap(*args, ** kwargs):
            if request.method != "POST":
                return jsonify({"error": True, "message": "POST request required"}), 400

            if request.method == "POST" and not request.json:
                return jsonify({"error": True, "message": "Please send JSON request"}), 400
            request_data = request.json
            error_response = check_for_required_fields(request_data, required_keys)
            if error_response.get('error', None):
                return jsonify(error_response), 400

            return f(*args, ** kwargs)

        return wrap
    return decorator

def put_json_required(required_keys=[]):
    def decorator(f):
        @wraps(f)
        def wrap(*args, ** kwargs):
            if request.method != "PUT":
                return jsonify({"error": True, "message": "POST request required"}), 400

            if request.method == "PUT" and not request.json:
                return jsonify({"error": True, "message": "Please send JSON request"}), 400
            request_data = request.json
            error_response = check_for_required_fields(request_data, required_keys)
            if error_response.get('error', None):
                return jsonify(error_response), 400

            return f(*args, ** kwargs)

        return wrap
    return decorator

def query_params_required(required_keys=[]):
    def decorator(f):
        @wraps(f)
        def wrap(*args, ** kwargs):
            if request.method != "GET":
                return jsonify({"error": True, "message": "POST request required"}), 400

            if request.method == "GET" and not request.args:
                return jsonify({"error": True, "message": "Please send JSON request"}), 400
            request_data = request.args
            error_response = check_for_required_fields(request_data, required_keys)
            if error_response.get('error', None):
                return jsonify(error_response), 400

            return f(*args, ** kwargs)

        return wrap
    return decorator


def form_required(required_keys=[]):
    def decorator(f):
        @wraps(f)
        def wrap(*args, ** kwargs):
            if request.method != "POST":
                return jsonify({"error": True, "message": "POST request required"}), 400

            if request.method == "POST" and not request.form:
                return jsonify({"error": True, "message": "Please send form request"}), 400
            request_data = request.form
            error_response = check_for_required_fields(request_data, required_keys)
            if error_response.get('error', None):
                return jsonify(error_response), 400

            return f(*args, ** kwargs)

        return wrap
    return decorator
