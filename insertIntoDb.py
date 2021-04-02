
def insertTweetNumber(database, Leader, tweetId):
    query = ("INSERT OR REPLACE INTO "+Leader+"tweets (tweetId) VALUES(" + str(tweetId) + ")")
    database.execute(query)

def insertProfileDetails(leader,type, profileDetailList):
    pass

def insertEdge(country):
    pass
