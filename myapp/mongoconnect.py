from pymongo import MongoClient
import os
#CODE_TYPE = os.environ['CODE_TYPE']
CODE_TYPE = os.environ.get('CODE_TYPE', "dev")

def connect_to_mongo():
    if CODE_TYPE == "dev":
        client = MongoClient('localhost', 27017)
        return client.dev_db
    elif CODE_TYPE == "prod":
        client = MongoClient("mongodb://uname:pwd@localhost/admin")
        return client.prod_db
