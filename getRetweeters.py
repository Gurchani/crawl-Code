import createDatabase
import json
import insertIntoDb
def getTweets(leader, database):
    Query = 'Select tweetId from ' + str(leader) + 'tweets'
    tweets = database.execute(Query)
    return tweets

def Retweeters(TwitterConnection, tweet):
    call = 'https://api.twitter.com/1.1/statuses/retweeters/ids.json?id=' \
           +str(tweet[0])+'&count=100&stringify_ids=true'
    response2, data2 = TwitterConnection.request(call)
    retweeters = json.loads(data2)
    if response2.status == 200:
        return retweeters
    elif response2.status == 429:
        print('Met the 15min Authentication Limit')
    else:
        print('There is some problem, read the following Twitter error code:')
        print(response2.status)



def getRetweeters(TwitterConnection, leaderNames, db):
    for i in leaderNames:
        createDatabase.createRetweetertab(i, db)
        for k in getTweets(i, db):
            retweeters = Retweeters(TwitterConnection, k)
            if retweeters is not None:
                insertIntoDb.insertRetweeters(str(k[0]), retweeters, i, db)
            else:
                print(k[0])




