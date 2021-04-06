import  connectToTwitter
import  json
import createDatabase
import  insertIntoDb

apiVersion1Call = 'https://api.twitter.com/1.1/friends/ids.json'

def getUsers(party, db):
    Query = 'Select retweeterId from ' + party + 'retweeterFreq'
    listToReturn = []
    for k in db.execute(Query):
        listToReturn.append(k[0])
    return listToReturn

def insertFriendEdges(user, party, FriendsData, db):
    createDatabase.createRetweeterFriendsDb(party, db)
    for k in FriendsData["ids"]:
        insertIntoDb.insertRetweeterFriends(user, party, k, db)


def getFriends(userList, party, db):
    for i in userList:
        cursor = -1
        while cursor is not 0:
            friendCall = apiVersion1Call+"?cursor="+str(cursor)+"&user_id="+str(i)+"&count=5000"
            global TwitterClient
            response2, data2 = TwitterClient.request(friendCall)
            if response2.status == 200:
                FriendsData = json.loads(data2)
                insertFriendEdges(i, party, FriendsData, db)
                cursor = FriendsData["next_cursor"]
            elif response2.status == 429:
                print('Previous authentication stopped working')
                TwitterClient = connectToTwitter.connect2()
            else:
                print('Try to print the new error code')






def crawl(parties, db):
    global TwitterClient
    TwitterClient = connectToTwitter.connect2()
    for i in parties:
        UsersList = getUsers(i, db)
        getFriends(UsersList, i, db)

#Testing Code
#databseLocation = "C:\sqlite\db\\"
#desiredReferanceScore = input('What percentage of graph you want:')
#country = input('Country Name:')
#db = createDatabase.createCountrydb(country, databseLocation)
#crawl(['PTI'], db)