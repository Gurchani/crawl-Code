import  connectToTwitter
import  json
import createDatabase
import  insertIntoDb

apiVersion1Call = 'https://api.twitter.com/1.1/followers/ids.json'

def insertSeedFollowerEdges(user, party, FollowerData, db):
    createDatabase.createSeedFollowerDb(party, db)
    for k in FollowerData["ids"]:
        insertIntoDb.insertSeedFollower(user, party, k, db)



def getFollowers(seeds, party, db):
        for l, j in zip(seeds, party):
            for i in l:
                print('Getting friends of User :' + str(i))
                cursor = -1
                while cursor != 0:
                    followerCall = apiVersion1Call + "?cursor=" + str(cursor) + "&user_id=" + str(i) + "&count=5000"
                    global TwitterClient
                    response2, data2 = TwitterClient.request(followerCall)
                    if response2.status == 200:
                        FollowerData = json.loads(data2)
                        insertSeedFollowerEdges(i, j, FollowerData, db)
                        cursor = FollowerData["next_cursor"]
                    elif response2.status == 429:
                        print('Previous authentication stopped working')
                        TwitterClient = connectToTwitter.connect3()
                    else:
                        print(response2.status)
                        print('Try to print the new error code')


getFollowers([122453931, 3234394240], 'PTI')