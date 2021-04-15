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

def createSeedFollowerDb(party, database):
    queryText = 'Create table IF NOT EXISTS ' + str(party) + 'seedFollowers (SeedId BIGINT,' \
                                                             'FollowerId BIGINT NOT NULL)'
    database.execute(queryText)

def createTweetIdtab(leader, database):
    queryText = 'Create table IF NOT EXISTS '+str(leader)+'tweets (tweetId BIGINT PRIMARY KEY)'
    database.execute(queryText)

def createUserDetailtab(db):
    queryText = 'create table if not exists userdetails (id BIGINT PRIMARY KEY,' \
                'id_str STRING, name STRING, screen_name STRING, location STRING,description STRING, protected BOOLEAN,' \
                'verified BOOLEAN, followers_count INTEGER, friends_count INTEGER, favourites_count INTEGER,' \
                'statuses_count INTEGER, created_at INTEGER )'
    db.execute(queryText)


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
