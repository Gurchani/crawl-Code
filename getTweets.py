import errno

import oauth2 as oauth
import json
import unicodedata
import pymysql


apiVersion2Call = 'https://api.twitter.com/2/users/:id/tweets'
apiVersion1Call = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

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

def connectToTwitter():
    import connectToTwitter
    credentials = connectToTwitter.connect()
    print(credentials)
    consumer = oauth.Consumer(key=credentials[0], secret=credentials[1])
    access_token = oauth.Token(key=credentials[2], secret=credentials[3])
    client = oauth.Client(consumer, access_token)
    return client


def getTweets(id, client):
    gatheredTweets = []
    cursor = 0
    maxId = 0
    timeTobreak = False
    for l in range(0, 20):
        if maxId is not 0:
            recentTweets = apiVersion1Call + "?cursor=" + str(cursor) + "&user_id=" + str(
                id) + "&count=200&include_rts=0&max_id=" + str(maxId)
        else:
            recentTweets = apiVersion1Call + "?cursor=" + str(cursor) + "&user_id=" + str(
                id) + "&count=200&include_rts=1"
        response2, data2 = client.request(recentTweets)
        tweets = json.loads(data2)
        if len(tweets) < 150:
            gatheredTweets.append(tweets)
            return gatheredTweets

        if response2.status == 200:
            gatheredTweets.append(tweets)
            for k in tweets:
                idVal = k['id']
                if maxId > idVal or maxId == 0:
                    maxId = idVal
        else:
            print(id)
            print(len(gatheredTweets))
            return gatheredTweets
def insertIntoDb(database , Leader, tweetId):
    query = ("INSERT INTO Elitetweets (tweetId) VALUES(" + str(tweetId)+")")
    database.execute(query)


if __name__ == '__main__':
    db = create_connection(r"C:\sqlite\db\pythonsqlite.db")
    db.execute('Create table IF NOT EXISTS Elitetweets (tweetId BIGINT PRIMARY KEY)')
    TwitterClient = connectToTwitter()
    Leaders = input('Twitter handle of the Leader')
    requestTweets = getTweets(id, TwitterClient)
    for j in requestTweets:
        for k in j:
            try:
                insertIntoDb(db, Leaders, k['id'])
            except:
                'Error inserting'
    #test
    query2 = ('Select tweetId from Elitetweets')
    for i in db.execute(query2):
        print(i[0])
