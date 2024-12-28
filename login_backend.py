# backend.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy user data
users = {
    "admin": "password"
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username == 'junzheyi' and password == '123456':
        return jsonify({"success": True, "message": "Logged in successfully!"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)