import sqlite3


def get_db_connection():
    connection = sqlite3.connect("sql_pizza.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = sqlite3.connect("sql_pizza.db")
    with open("schema.sql") as f:
        connection.executescript(f.read())