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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """verification of password"""
    return bcrypt.checkpw(password.encode('UTF-8'),
                          hashed_password)
