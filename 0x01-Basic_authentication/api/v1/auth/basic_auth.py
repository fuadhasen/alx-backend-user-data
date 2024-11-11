#!/usr/bin/env python3
"""  module for BasiAuth
"""
from flask import request
from .auth import Auth
from typing import List, TypeVar


class BasicAuth(Auth):
    """Basic Authentication Simulation
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """base64 decoding"""
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        value = authorization_header.split(' ')[1]
        return value
