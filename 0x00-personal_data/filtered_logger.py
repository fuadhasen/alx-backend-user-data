#!/usr/bin/env python3
"""script for filtered logger"""
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    """function filter_datum"""
    for field in fields:
        message = re.sub(rf"{field}=[^{separator}]*",
                         f"{field}={redaction}", message)
    return separator.join(message.split(separator))
