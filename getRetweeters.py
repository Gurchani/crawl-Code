import createDatabase
import json
import insertIntoDb
def getTweets(leader, database):
    Query = 'Select tweetId from ' + str(leader) + 'tweets'
    tweets = database.execute(Query)
    return tweets

def Retweeters(tweet):
    call = 'https://api.twitter.com/1.1/statuses/retweeters/ids.json?id=' \
           +str(tweet[0])+'&count=100&stringify_ids=true'
    global TwitterClient
    response2, data2 = TwitterClient.request(call)
    retweeters = json.loads(data2)
    if response2.status == 200:
        return retweeters
    elif response2.status == 429:
        TwitterClient = connectToTwitter.connect3()
        print('Met the 15min Authentication Limit')
    else:
        print('There is some problem, read the following Twitter error code:')
        print(response2.status)
        TwitterClient = connectToTwitter.connect3()


import connectToTwitter
import getLeaderNames
def getRetweeters(leaderNames, parties, db):
    global TwitterClient
    TwitterClient = connectToTwitter.connect3()
    partyLeaderDf = getLeaderNames.getLeaderPartyDF(leaderNames, parties)
    print(partyLeaderDf)
    parties = partyLeaderDf['party'].unique()
    for l in parties:
        createDatabase.createRetweetertab(l, db)
        leaderNames = partyLeaderDf[partyLeaderDf['party'] == l]['leader']
        for i in leaderNames:
            counter = 0 #Remove
            for k in getTweets(i, db):
                counter = counter + 1 #Remove
                if counter > 20: #Remove
                    break        #Remove
                retweeters = Retweeters(k)
                if retweeters is not None:
                    insertIntoDb.insertRetweeters(str(k[0]), retweeters, l, db)
                else:
                    print(k[0])




