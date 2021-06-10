from flask import Flask, request, render_template
import secrets
import os
import stripe
#CODE_TYPE = os.environ['CODE_TYPE']
CODE_TYPE  = os.environ.get("CODE_TYPE", "dev")

secret = secrets.token_urlsafe(32)

app = Flask(__name__)

app.debug = True
if CODE_TYPE == "prod":
    app.debug = False

@app.route('/')
def hello():
    return "Hello"
@app.route('/abc')
def helloabc():
    return render_template("a.html")

from myapp import menu_management, orders_management, table_management

#from myapp.API.v1 import accounts

menu_management.Initialize(app)
'''orders_management.Initialize(app)'''
table_management.Initialize(app)

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method  == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT, HEAD, FETCH, OPTIONS'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers

    # Batch log
    return response
app.after_request(add_cors_headers)

#def before_request():
#    '''from myapp.core.middlewares.common_middleware import common_middleware
#    common_middleware()''' # commenting middle ware code for now
#
#app.before_request(before_request)
