
from flask import Flask, request, jsonify
from flask_cors import CORS
from login import api_user

app = Flask(__name__)
CORS(app)

@app.route('/fetch', methods=['POST', 'GET'])
def fetch_data():
    if request.method == 'POST':
        json = request.get_json()
        api = api_user(json['user_id'], json['body'], json['api_path'])
        return jsonify(api)
    else:
        return {}
