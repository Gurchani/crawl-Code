
import  connectToTwitter
import json
import createDatabase
import insertIntoDb
apiCall = 'https://api.twitter.com/1.1/users/lookup.json'

def insertIntoDatabase(profileDetails, db):
    insertIntoDb.insertProfileDetails(profileDetails, db)


def callAPI(IdString, db):
    global TwitterClient
    TwitterClient = connectToTwitter.connect3()
    call = apiCall + '?user_id=' + IdString
    response2, data2 = TwitterClient.request(call)
    if response2.status == 200:
        insertIntoDatabase(data2, db)
    elif response2.status == 429:
        TwitterClient = connectToTwitter.connect3()
    else:
        print('Twitter Response is: ')
        print(response2.status)


def getProfileDetails(users, db):
    createDatabase.createUserDetailtab(db)
    global TwitterClient
    TwitterClient = connectToTwitter.connect3()
    listOfId = ''
    for i, count in zip(users, range(0, len(users))):
        listOfId = listOfId + str(i)
        if count % 100 == 0:
            callAPI(listOfId, db)
            listOfId = ''
    if listOfId != '':
        callAPI(listOfId, db)


#import createDatabase
#databseLocation = "C:\sqlite\db\\"
#desiredReferanceScore = input('What percentage of graph you want:')
#country = input('Country Name:')
#db = createDatabase.createCountrydb(country, databseLocation)

#parties = ['217749896', '14973943']
#seedsBasic = getProfileDetails(parties, db)
#for i in db.execute('select * from userdetails'):
#    print(i)
#validateSeed(parties, seedsBasic, db, 50)



