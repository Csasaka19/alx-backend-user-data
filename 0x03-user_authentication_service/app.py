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