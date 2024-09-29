from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask API!")

@app.route('/api/session_id', methods=['GET'])
def get_data():
    session = requests.Session() 

    response = session.get('http://aspen.cpsd.us/aspen/logon.do') 
    
    return {'session_id': session.cookies.get_dict().get('JSESSIONID')}

@app.route('/api/data', methods=['POST'])
def post_data():
    new_data = request.json
    return jsonify(new_data), 201

if __name__ == '__main__':
    app.run(debug=True)