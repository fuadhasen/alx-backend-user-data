#!/usr/bin/env python3
"""  module for BasiAuth
"""
import base64
from flask import request
from .auth import Auth
from typing import List, TypeVar, Tuple
from models.base import Base
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication Simulation
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract authorization header"""
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        value = authorization_header.split(' ')[1]
        return value

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """base64 Decodings"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_val = base64.b64decode(base64_authorization_header)
            return decoded_val.decode('UTF-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """extract user credentials from authorization header"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, pwd = decoded_base64_authorization_header.split(':')
        return (email, pwd)


    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> 'User':
        """User from credential"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            user_list = User.search({'email': user_email})
        except Exception:
            return None
        
        if len(user_list) == 0:
            return None
        for user in user_list:
            if user.is_valid_password(user_pwd) is True:
                return user
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """override Auth and retreive authenticated user instance 
        """
        # You must use authorization_header
        header = self.authorization_header(request)
        # You must use extract_base64_authorization_header
        value = self.extract_base64_authorization_header(header)
        # You must use decode_base64_authorization_header
        credentials = self.decode_base64_authorization_header(value)
        # You must use extract_user_credentials
        email, pwd = self.extract_user_credentials(credentials)
        # You must use user_object_from_credentials
        user = self.user_object_from_credentials(email, pwd)
        return user
