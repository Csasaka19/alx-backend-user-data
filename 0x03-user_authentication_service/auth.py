#!/usr/bin/env python3
'''This is the auth module'''
import bcrypt

def _hash_password(password: str) -> str:
    '''Method that takes in a password string arguments and returns a
    bytes'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())