#!/usr/bin/env python3
"""Authentication module
"""
import bcrypt
from user import User
from db import DB
from typing import Union
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """hashing password"""
    hashed_pwd = bcrypt.hashpw(
        password.encode('UTF'), bcrypt.gensalt()
    )
    return hashed_pwd


def _generate_uuid() -> str:
    """function to generate UUID
    """
    import uuid
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """method to register user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError
        except NoResultFound:
            hashed = _hash_password(password)
            user = self._db.add_user(email, hashed)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """valid login method
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                if bcrypt.checkpw(password.encode('UTF'),
                                  user.hashed_password):
                    return True
                return False
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """method to create session on server
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """method to fetch user from session_id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int):
        """destroy session from the database
        """
        return self._db.update_user(user_id, **{'session_id': None})

    def get_reset_password_token(self, email: str) -> str:
        """reset password token generator
        """
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            raise ValueError

        id = _generate_uuid()
        self._db.update_user(user.id, **{'reset_token': id})
        return id

    def update_password(self, reset_token: str, password: str) -> None:
        """update password method
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except (NoResultFound, InvalidRequestError):
            raise ValueError

        hashed = _hash_password(password)
        user.hashed_password = hashed
        user.reset_token = None
        return None
