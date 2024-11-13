#!/usr/bin/env python3
"""  module for Authentication
"""
from os import getenv
from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """ class for authenticating user of the app
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ paths that require authentication
        """
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        if path is None:
            return True

        n_path = path.rstrip('/')
        for p in excluded_paths:
            n_p = p.rstrip('/')
            if n_path == n_p:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header method
        """
        if request is None:
            return None

        if not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def session_cookie(self, request=None):
        """session cookies
        """
        if request is None:
            return None
        session_id = getenv('SESSION_NAME')
        return request.cookies.get(session_id)
        

    def current_user(self, request=None) -> 'User':
        return None
