#!/usr/bin/env python3
"""  module for BasiAuth
"""
from flask import request
from .auth import Auth
from typing import List, TypeVar


class BasicAuth(Auth):
    """Basic Authentication Simulation
    """
    pass
