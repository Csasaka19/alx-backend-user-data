#!/usr/bin/env python3
"""Encrypting passwords module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Method that returns a salted, hashed password, which is a byte string"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Method that expects 2 arguments and returns a boolean"""
    return bcrypt.checkpw(password.encode(), hashed_password)