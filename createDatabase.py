import sqlite3
from sqlite3 import Error

def createProfileDetailtab(leader):
    pass

def createCoverTable(party, db):
    queryText = 'Create table IF NOT EXISTS ' + str(party) + 'covered (retweeterId BIGINT)'
    db.execute(queryText)

def createRetweeterFriendsDb(party, database):
    queryText = 'Create table IF NOT EXISTS ' + str(party) + 'retweeterFriends (retweeterId BIGINT,' \
                                                              'FriendId BIGINT NOT NULL)'
    database.execute(queryText)

def createTweetIdtab(leader, database):
    queryText = 'Create table IF NOT EXISTS '+str(leader)+'tweets (tweetId BIGINT PRIMARY KEY)'
    database.execute(queryText)



def createRetweetertab(leader, database):
    queryText = 'Create table IF NOT EXISTS ' + str(leader) + 'retweeters (tweetId BIGINT,' \
                                                              'retweeterId BIGINT NOT NULL)'
    database.execute(queryText)


def createNetworkGraphtab(country):
    pass

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

def createCountrydb(country, loc):
    tempString = loc + country + ".db"
    print(tempString)
    db = create_connection(tempString)
    return db
