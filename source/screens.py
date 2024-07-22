
from flask import Flask, request, jsonify
from flask_cors import CORS
from login import api_user
app = Flask(__name__, static_folder='../static')
CORS(app)
@app.route('/fetch', methods=['POST', 'GET'])
def fetch_data():
    if request.method == 'POST':
        json = request.get_json()
        print(json)
        api = api_user(json['user_id'], json['body'], json['api_path'])
        return jsonify(api)
    else:
        return {}




'''
import json
@app.route('/tables_updates', methods=['POST', 'GET'])
def tables_updates():
    with open('local_files/depends.json', 'r', encoding='utf-8') as file:
        info = json.load(file)
    
    return info

@app.route('/event', methods=['POST', 'GET'])
def event():
    if request.method == 'POST':
        json = request.get_json()
        event_info = api_event(json['user_id'], json['body'])
        return jsonify(event_info)
    else:
        return {}

@app.route('/tamplate', methods=['POST', 'GET'])
def tamplate():
    global all_tamplate
    if request.method == 'POST':
        json = request.get_json()
        print(json)
        tamplate_info = api_tampltes(**json)
        all_tamplate[json['tamplate']] = tamplate_info
        return tamplate_info
    else:
        return all_tamplate

@app.route('/screens', methods=['POST', 'GET'])
def screens():
    global all_tamplate
    if request.method == 'POST':
        json = request.get_json()
        screens_info = api_screens(**json)
        return screens_info
    else:
        return {}

        
all_tamplate = {}
test_check_account = {}


@app.route('/login', methods=['POST', 'GET'])
def login():
    global test_check_account
    if request.method == 'POST':
        json = request.get_json()
        check_account = api_login(json['name'], json['password'])
        test_check_account = check_account
        return check_account
    else:
        return test_check_account


'''
import time
print(time.time())
