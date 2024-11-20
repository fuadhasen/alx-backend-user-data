#!/usr/bin/env python3
"""Flask app module
"""
from flask import (Flask, jsonify, request,
                   make_response, abort,
                   redirect, url_for)
from auth import Auth
from db import DB
from sqlalchemy.orm.exc import NoResultFound

AUTH = Auth()


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Index route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """method to register usersl"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'])
def login():
    """method to login user"""
    email = request.form.get('email')
    password = request.form.get('password')

    ok = AUTH.valid_login(email, password)
    if not ok:
        abort(401)
    session_id = AUTH.create_session(email)
    resp = make_response({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@app.route('/sessions', methods=['DELETE'])
def logout():
    """method to logout user"""
    session_id = request.form.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """method to register usersl"""
    session_id = request.form.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
