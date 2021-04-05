
def insertTweetNumber(database, Leader, tweetId):
    query = ("INSERT OR REPLACE INTO "+Leader+"tweets (tweetId) VALUES(" + str(tweetId) + ")")
    database.execute(query)
    database.commit()

def insertProfileDetails(leader,type, profileDetailList):
    pass

def insertEdge(country):
    pass

def insertRetweeters(tweet, retweeters, Party, database):
    retweetersList = retweeters.get('ids')
    for j in retweetersList:
        query = ("INSERT INTO " + Party + "retweeters (tweetId, retweeterId) "
                                                      "VALUES(" + str(tweet) + ","+str(j)+")")
        database.execute(query)
        database.commit()

