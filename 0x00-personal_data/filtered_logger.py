#!/usr/bin/env python3
"""script for filtered logger"""
import re
import os
import logging
import mysql.connector
from typing import List
PII_FIELDS = ('ssn', 'email', 'name', 'pwd', 'phone')


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    """function filter_datum"""
    for field in fields:
        message = re.sub(rf"{field}=[^{separator}]*",
                         f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        messge = record.getMessage()
        filter_mssge = filter_datum(self.fields,
                                    self.REDACTION,
                                    messge, self.SEPARATOR)
        original_mssge = super().format(record)
        return original_mssge.replace(messge,
                                      filter_mssge)


def get_logger() -> logging.Logger:
    """create logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Implement get db function securely."""
    conn = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )

    return conn
