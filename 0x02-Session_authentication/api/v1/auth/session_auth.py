#!/usr/bin/env python3
"""  module for BasiAuth
"""
import base64
from flask import request
from .auth import Auth
from typing import List, TypeVar, Tuple
from models.base import Base
from models.user import User
import uuid


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
