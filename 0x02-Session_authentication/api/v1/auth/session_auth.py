#!/usr/bin/env python3
"""  module for BasiAuth
"""
from os import getenv
import base64
from flask import request
from .auth import Auth
from typing import List, TypeVar, Tuple
from models.base import Base
from models.user import User
import uuid
from models.user import User


class SessionAuth(Auth):
    """Session Authentication manual Implementation
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """instance method to create session
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = uuid.uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id
        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """return user_id based on session_id
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """override current user for session auth
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(session_id)
        user_instance = User.get(user_id)
        return user_instance

    def destroy_session(self, request=None):
        """custome logout implementation
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_by_session_id.get(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True

