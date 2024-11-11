#!/usr/bin/env python3
"""  module for BasiAuth
"""
import base64
from flask import request
from .auth import Auth
from typing import List, TypeVar


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
        """base64 Decoding"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_val = base64.b64decode(base64_authorization_header)
            return decoded_val.decode('UTF-8')
        except Exception:
            return None
