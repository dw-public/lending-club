"""
Methods to query loan data set from sqlite file
"""

import pandas as pd
import os

import sqlite3

# TODO extract to config and improve path handling
path_to_sql = 'data/lending-club-loan-data/database.sqlite'


def create_connection(db_path):
    """
    Create a connection to the SQLite db at the specified path
    Args:
        db_file: path to the database file

    Returns:
        Connection object or None

    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Exception as e:
        print(os.getcwd())

    return None


def sql_to_df(query):
    """
    Executes query against the sqlite file specified in db.py

    Args:
        query (str): Sql query

    Returns:
        Pandas dataframe of query results

    """
    conn = create_connection(path_to_sql)
    df = pd.read_sql(query, conn)
    conn.close()
    return df
