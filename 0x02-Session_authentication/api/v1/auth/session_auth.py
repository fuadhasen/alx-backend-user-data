#!/usr/bin/env python3
"""  module for BasiAuth
"""
import base64
from flask import request
from .auth import Auth
from typing import List, TypeVar, Tuple
from models.base import Base
from models.user import User


class SessionAuth(Auth):
    """Session Authentication manual Implementation
    """
    pass