
import  json
def insertTweetNumber(database, Leader, tweetId):
    query = ("INSERT OR REPLACE INTO "+Leader+"tweets (tweetId) VALUES(" + str(tweetId) + ")")
    database.execute(query)
    database.commit()

def insertSeedFollower(user,party,edge, db):
    query = ("Insert or replace into "+party+"seedFollowers (SeedId, FollowerId) VALUES ("+user+","+edge+")")
    db.execute(query)

def insertProfileDetails(profileDetailList, db):
    counter = 0
    profiles = json.loads(profileDetailList)
    InsertQuery = "INSERT OR IGNORE INTO userdetails (`id`, `id_str`,`name`, `screen_name`, `location`, `description`, `protected`, `verified`, `followers_count`, `friends_count`, `favourites_count`, `statuses_count`, `created_at`) " \
                  "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
    for k in profiles:
        values = (str(k.get("id")),
                      k.get("id_str"),
                  k.get("name").encode('ascii', 'ignore').decode('ascii'),
                  k.get("screen_name").encode('ascii', 'ignore').decode('ascii'),
                  k.get("location").encode('ascii', 'ignore').decode('ascii'),
                  k.get("description").encode('ascii', 'ignore').decode('ascii'),
                  str(k.get("protected")),
                  str(k.get("verified")),
                  k.get("followers_count"),
                  k.get("friends_count"),
                  k.get("favourites_count"),
                  k.get("statuses_count"),
                  k.get("created_at")

                  # k.get("lang")
                  )
        db.execute(InsertQuery, values)
        db.commit()
        #InsertQuery = ("INSERT OR IGNORE INTO userdetails (`id`, `id_str`,`name`, `screen_name`, `location`, `description`, `protected`, `verified`, `followers_count`, `friends_count`, `favourites_count`, `statuses_count`, `created_at`) "
        #               "VALUES " + values)

        counter = counter + 1

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

