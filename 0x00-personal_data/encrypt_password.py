#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hashing the user password"""
    hashed = bcrypt.hashpw(password.encode('UTF-8'),
                           bcrypt.gensalt())
    return hashed
