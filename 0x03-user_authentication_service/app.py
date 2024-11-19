#!/usr/bin/env python3
"""Flask app module
"""
from flask import Flask, jsonify, request
from auth import Auth
from db import DB

AUTH = Auth()


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Index route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """method to register usersl"""
    email = request.form.get('email')
    password = request.form.get('password')
    user_obj = DB()
    try:
        user = user_obj.find_user_by(email=email)
    except Exception:
        AUTH.register_user(email, password)
        return jsonify({"email": "<registered email>",
                        "message": "user created"})

    AUTH.register_user()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
