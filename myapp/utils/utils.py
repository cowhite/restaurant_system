from flask import jsonify, json, session



def myresponse(res):

    if type(res) == dict:
        if res.get('status_code', None) == 0:
            return jsonify(res), 400

    return jsonify(res)

def parse_json(data):
    if type(data) == list:
        for x in data:
            if '_id' in x:
                x['_id'] = str(x['_id'])
    else:
        if "_id" in data:
            data['_id'] = str(data['_id'])
    return data