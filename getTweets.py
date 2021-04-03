import errno

import oauth2 as oauth
import json
import createDatabase
import insertIntoDb
import unicodedata
import pymysql


apiVersion2Call = 'https://api.twitter.com/2/users/:id/tweets'
apiVersion1Call = 'https://api.twitter.com/1.1/statuses/user_timeline.json'


def connectToTwitter(credentials):
    consumer = oauth.Consumer(key=credentials[0], secret=credentials[1])
    access_token = oauth.Token(key=credentials[2], secret=credentials[3])
    client = oauth.Client(consumer, access_token)
    return client


def getEachTweets(id, client):
    gatheredTweets = []
    cursor = 0
    maxId = 0
    timeTobreak = False
    for l in range(0, 30):
        if maxId is not 0:
            recentTweets = apiVersion1Call + "?cursor=" + str(cursor) + "&screen_name=" + str(
                id) + "&count=200&include_rts=0&max_id=" + str(maxId)
        else:
            recentTweets = apiVersion1Call + "?cursor=" + str(cursor) + "&screen_name=" + str(
                id) + "&count=200&include_rts=1"
        response2, data2 = client.request(recentTweets)
        tweets = json.loads(data2)
        #print(response2.status)
        #if len(tweets) < 150:
        #    gatheredTweets.append(tweets)
        #    return gatheredTweets

        if response2.status == 200:
            #print(len(tweets))
            #gatheredTweets.append(tweets)
            print(len(gatheredTweets))
            for k in tweets:
                gatheredTweets.append(k)
                idVal = k['id']
                if maxId > idVal or maxId == 0:
                    maxId = idVal
        else:
            print(response2.status)
            print(id)
            print(len(gatheredTweets))
            #gatheredTweets.append(tweets)
            return gatheredTweets
    return gatheredTweets

def getTweets(TwitterClient, leaderNames, database):
    for leader in leaderNames:
        createDatabase.createTweetIdtab(leader, database)
        #TwitterClient = connectToTwitter(credentials)
        requestTweets = getEachTweets(leader, TwitterClient)
        print(requestTweets[0])
        for k in requestTweets:
            print(k.get('id'))
            try:
               insertIntoDb.insertTweetNumber(database,leader, k.get('id'))
            except Exception as e:
               print(e.message, e.args)
        #test
        totalTweets = []
        query2 = ('Select tweetId from '+leader+'tweets')
        for i in database.execute(query2):
            totalTweets.append(i[0])
        print(leader)
        print(len(totalTweets))
