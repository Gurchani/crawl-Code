import  connectToTwitter
import  json
import createDatabase
import  insertIntoDb
import time

apiVersion1Call = 'https://api.twitter.com/1.1/followers/ids.json'

def insertSeedFollowerEdges(user, party, FollowerData, db):
    createDatabase.createSeedFollowerDb(party, db)
    for k in FollowerData["ids"]:
        insertIntoDb.insertSeedFollower(user, party, k, db)

def TimeRemaining(response):
    try:
        print(response)
        limit = int(response.get("x-rate-limit-limit"))
        remaining = int(response.get("x-rate-limit-remaining"))
        timeToReset = int(response.get("x-rate-limit-reset"))

        if remaining/limit > 0.1:
            return True
        else:
            return False
    except:
        return False

def getFollowers(seeds, party, db):
        for l, j in zip(seeds, party):
            for i in l:
                print('Getting friends of User :' + str(i))
                counter = 0
                cursor = -1
                while cursor != 0:
                    followerCall = apiVersion1Call + "?cursor=" + str(cursor) + "&user_id=" + str(i) + "&count=5000"
                    global TwitterClient
                    TwitterClient = connectToTwitter.connect3()
                    response2, data2 = TwitterClient.request(followerCall)
                    if response2.status == 200 and TimeRemaining(response2):
                        FollowerData = json.loads(data2)
                        insertSeedFollowerEdges(i, j, FollowerData, db)
                        cursor = FollowerData["next_cursor"]
                    elif response2.status == 429:
                        time.sleep(30)
                        print('Previous authentication stopped working')
                        TwitterClient = connectToTwitter.connect3()
                    elif response2.status == 401:
                         cursor = 0
                         print('User is locked')
                    else:
                        counter = counter + 1
                        if counter > 2:
                            cursor = 0
                        time.sleep(30)
                        print(response2.status)
                        print('Try to print the new error code')


#Testing Code
#databseLocation = "C:\sqlite\db\\"
#desiredReferanceScore = input('What percentage of graph you want:')
#country = input('Country Name:')
#db = createDatabase.createCountrydb(country, databseLocation)
#getFollowers([[122453931, 3234394240]], ['JUIF'], db)