#!/usr/bin/env python3
"""Authentication module
"""
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hashing password"""
    hashed_pwd = bcrypt.hashpw(
        password.encode('UTF'), bcrypt.gensalt()
    )
    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """method to register user
        """
        user_obj = DB()

        try:
            user = user_obj.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed = _hash_password(password)
            user = self._db.add_user(email, hashed)

        return user
