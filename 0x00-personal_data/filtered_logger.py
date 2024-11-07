#!/usr/bin/env python3
"""script for filtered logger"""
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str):
    """function filter_datum"""
    for field in fields:
        match = rf"{field}=[^{separator}]*"
        replacment_pattern = f"{field}={redaction}"
        message = re.sub(match, replacment_pattern, message)
    return message
