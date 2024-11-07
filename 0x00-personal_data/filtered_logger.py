#!/usr/bin/env python3
"""script for filtered logger"""
import re
import os
import logging
import mysql.connector
from typing import List
PII_FIELDS = ('ssn', 'email', 'name', 'password', 'phone')


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
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        filter_mssge = filter_datum(self.fields,
                                    self.REDACTION,
                                    record.getMessage(), self.SEPARATOR)
        record.msg = filter_mssge
        return super().format(record)


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


def get_db():
    """Implement get db function securely."""
    conn = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )

    return conn


def main():
    """main function"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, email, phone,\
        ssn, password, ip, last_login, user_agent \
        FROM users"
        )

    rows = cursor.fetchall()
    for row in rows:
        log_message = (
            f'name={row[0]}; email={row[1]}; phone={row[2]}; '
            f'ssn={row[3]}; password={row[4]}; '
            f'ip={row[5]}; last_login={row[6]}; '
            f'user_agent={row[7]}'
        )
        log_record = logging.LogRecord("my_logger", logging.INFO, None, None,
                                       log_message, None, None)
        formatter = RedactingFormatter(fields=PII_FIELDS)
        print(formatter.format(log_record))


if __name__ == "__main__":
    main()
