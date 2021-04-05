import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn

connection = create_connection("C:\sqlite\db\Pakistan.db")
Query = ('Select * from FNretweeters')
for i in connection.execute(Query):
    print(i)