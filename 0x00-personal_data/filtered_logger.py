#!/usr/bin/env python3
"""Filter data module"""
import logging
import re
import os
import mysql.connector
from typing import List


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """Function that returns the log message obfuscated"""
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    FIELDS_FORMAT = "({})".format('|'.join(PII_FIELDS))

    def __init__(self, fields: List[str]):
        """Constructor method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Method that returns a log"""
        return filter_datum(
            self.FIELDS_FORMAT, self.REDACTION,
            super(RedactingFormatter, self).format(record),
            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Method that returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Method that returns a connector to a database"""
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_database = os.getenv("PERSONAL_DATA_DB_NAME")
    connection = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_database,
        port=3306
    )
    return connection


def main():
    """Main function that retrieves and filters data"""
    fields = ("name", "email", "phone", "ssn", "password")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        message = "name={}; email={}; phone={}; ssn={}; password={};\
ip={}; last_login={}; user_agent={}; ".format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
