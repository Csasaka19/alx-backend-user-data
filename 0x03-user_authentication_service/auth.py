#!/usr/bin/env python3
'''This is the auth module'''
import bcrypt
from db import DB
from user import User
from uuid import uuid4

def _hash_password(password: str) -> str:
    '''Method that takes in a password string arguments and returns a
    bytes'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def _generate_uuid() -> str:
    '''Method that returns a string representation of a new UUID'''
    return str(uuid4())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
        
    def register_user(self, email: str, password: str) -> User:
        '''Method that takes mandatory email and password string arguments
        and returns a User object stored in the database'''
        if self._db.find_user_by(email=email):
            raise ValueError('User {} already exists'.format(email))
        else:
            return self._db.add_user(email, _hash_password(password))
    
        
        