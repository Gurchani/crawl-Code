
def insertTweetNumber(database, Leader, tweetId):
    query = ("INSERT OR REPLACE INTO "+Leader+"tweets (tweetId) VALUES(" + str(tweetId) + ")")
    database.execute(query)
    database.commit()

def insertProfileDetails(leader,type, profileDetailList):
    pass

def insertEdge(country):
    pass

def insertRetweeterFriends(user, party, friend, database):
    Query = ('INSERT INTO ' + party + 'retweeterFriends (retweeterId, FriendId) VALUES('+str(user) + ','+str(friend)+')')
    database.execute(Query)
    database.commit()


def insertRetweeters(tweet, retweeters, Party, database):
    retweetersList = retweeters.get('ids')
    for j in retweetersList:
        query = ("INSERT INTO " + Party + "retweeters (tweetId, retweeterId) "
                                                      "VALUES(" + str(tweet) + ","+str(j)+")")
        database.execute(query)
        database.commit()

