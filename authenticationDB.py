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

authentication = create_connection("/Users/anr-dis-covid/Desktop/sqlite/db/AuthenticationJune2021.db")

createAuthenticationDb = ('Create table IF NOT EXISTS authentication (CONSUMER_KEY Text,'
                          'CONSUMER_SECRET Text, ACCESS_KEY Text, ACCESS_SECRET)')

createAuthenticationDbTimer = ('Create table IF NOT EXISTS authenticationTimer (CONSUMER_KEY Text, followerTime, friendTime, tweetTime, profileDetailsTime)')

# authentication.execute(createAuthenticationDb)
#
# for i in range(0, 38):
#         CONSUMER_KEY = input('CONSUMER_KEY:')
#         CONSUMER_SECRET = input('CONSUMER_SECRET:')
#         ACCESS_KEY = input('ACCESS_KEY:')
#         ACCESS_SECRET = input('ACCESS_SECRET:')
#         InsertIntoAuthenticationDB = ('insert into authentication (CONSUMER_KEY '
#                                       ', CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET) VALUES ('+
#                                         CONSUMER_KEY+','+CONSUMER_SECRET+','+ ACCESS_KEY +
#                                       ','+ACCESS_SECRET +')')
#
#         print(InsertIntoAuthenticationDB)
#         authentication.execute(InsertIntoAuthenticationDB)
#         authentication.commit()

def Authentications():
    Query = 'Select * from authentication order by RANDOM() limit 15'
    for i in authentication.execute(Query):
        print(i)
        return [i[0], i[1], i[2], i[3]]

#Authentications()