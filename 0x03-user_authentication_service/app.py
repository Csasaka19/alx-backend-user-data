#!/usr/bin/env python3
'''This is the app module'''
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app_route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    '''Method that returns a message for the index page'''
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    '''Method that registers a user'''
    try:
        email = request.form['email']
        password = request.form['password']
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email,
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
