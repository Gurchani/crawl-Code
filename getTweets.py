import errno

import oauth2 as oauth
import json
import createDatabase
import insertIntoDb
import connectToTwitter
import time
import unicodedata
import pymysql


apiVersion2Call = 'https://api.twitter.com/2/users/:id/tweets'
apiVersion1Call = 'https://api.twitter.com/1.1/statuses/user_timeline.json'



def getEachTweets(id):
    gatheredTweets = []
    cursor = 0
    maxId = 0
    timeTobreak = False
    for l in range(0, 30):
        if maxId != 0:
            recentTweets = apiVersion1Call + "?cursor=" + str(cursor) + "&screen_name=" + str(
                id) + "&count=200&include_rts=0&max_id=" + str(maxId)
        else:
            recentTweets = apiVersion1Call + "?cursor=" + str(cursor) + "&screen_name=" + str(
                id) + "&count=200&include_rts=1"
        global TwitterClient
        response2, data2 = TwitterClient.request(recentTweets)
        tweets = json.loads(data2)
        #print(response2.status)
        #if len(tweets) < 150:
        #    gatheredTweets.append(tweets)
        #    return gatheredTweets

        if response2.status == 200 and TimeRemaining(response2):
            #print(len(tweets))
            #gatheredTweets.append(tweets)
            print(len(gatheredTweets))
            for k in tweets:
                gatheredTweets.append(k)
                idVal = k['id']
                if maxId > idVal or maxId == 0:
                    maxId = idVal
        elif response2.status == 429 or response2.status == 403:
            time.sleep(30)
            TwitterClient = connectToTwitter.connect3()
        else:
            print(response2.status)
            time.sleep(30)
            print(len(gatheredTweets))
            #gatheredTweets.append(tweets)
            return gatheredTweets
    return gatheredTweets

def TimeRemaining(response):
    try:
        print(response)
        limit = int(response.get("x-rate-limit-limit"))
        remaining = int(response.get("x-rate-limit-remaining"))
        timeToReset = int(response.get("x-rate-limit-reset"))

        if remaining / limit > 0.1:
            return True
        else:
            return False
    except:
        return False

def getTweets(leaderNames, database):
    for leader in leaderNames:
        createDatabase.createTweetIdtab(leader, database)
        global TwitterClient
        TwitterClient = connectToTwitter.connect3()
        requestTweets = getEachTweets(leader)
        print(requestTweets[0])
        for k in requestTweets:
            #print(k.get('id'))
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
        print('Number of Total Tweets Gathered')
        print(len(totalTweets))
