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

connection = create_connection("E:\Twitter Country Data\SWEDEN2.db")

Query = ('SELECT FriendId, count(*) as freq FROM KDretweeterFriends group by FriendId order by freq desc')
count = 0
for i in connection.execute(Query):
    count = count + 1
    print(i)

print('Number of Values returned')
print(count)

