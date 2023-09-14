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

    def valid_login(self, email: str, password: str) -> bool:
        '''Method that takes email and password string arguments and
        returns a boolean'''
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        '''Method that takes an email string argument and returns the session
        ID as a string'''
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        '''Method that takes a single session_id string argument and
        returns the corresponding User or None'''
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        '''Method that takes a single user_id integer argument and returns
        None'''
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        '''Method that takes an email string argument and returns a string'''
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        '''Method that takes reset_token string argument and a password
        string argument and returns None'''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)
        except Exception:
            raise ValueError
