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
Query = ('Select * from PTIretweeterFriends where retweeterId = 1269241567434420224')
count = 0
for i in connection.execute(Query):
    count = count + 1
    print(i)
print('Number of Values returned')
print(count)