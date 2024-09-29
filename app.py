from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask API!")

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'name': 'Sample Data',
        'value': 123
    }
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def post_data():
    new_data = request.json
    return jsonify(new_data), 201

if __name__ == '__main__':
    app.run(debug=True)