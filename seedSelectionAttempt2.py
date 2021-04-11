import pandas as pd
from pandas import DataFrame
import getProfileDetails
def getCrawlCost(users, db):
    getProfileDetails.getProfileDetails(users,db )
    followerCount = []
    for i in users:
        query = 'select id, followers_count from userdetails where id = ' + str(i)
        for k in db.execute(query):
            print(k[0])
            followerCount.append([k[0], k[1]])
    return pd.DataFrame(followerCount, columns=['id', 'crawlCost'])

def getDataOfRetweetersFriends(party, db):
    Query = "Select * from " + party + "retweeterFriends"
    recoverall = db.execute(Query)
    df = DataFrame(recoverall.fetchall())
    df.columns = ['retweeterId', 'friend']
    return df

import itertools
def getRetweeterCombos(uniqueRetweeters):
    combos = []
    for i in range(int(len(uniqueRetweeters)/1.5), len(uniqueRetweeters)):
        combos.append(list(itertools.combinations(uniqueRetweeters, i)))
    return combos
def getGoodSeeds(parties, combos, dicOfSets):
    for party in combos:


def selectSeed(parties, db, NumberOfRetweeters):
    allFriends = []
    dicOfSets = {}
    retweeterCombos = []
    for i in parties:
        partyDf = getDataOfRetweetersFriends(i, db)
        uniqueRetweeters = list(partyDf['retweeterId'].unique())
        allFriends.append(partyDf['friend'].unique())
        for j in uniqueRetweeters:
            dicOfSets[j] = set(partyDf[partyDf['retweeterId'] == j]['friend'])
        combinationsOfRetweeters = getRetweeterCombos(uniqueRetweeters)
        retweeterCombos.append(combinationsOfRetweeters)

    getGoodSeeds(retweeterCombos, dicOfSets)

import createDatabase
print('asdasd')
databseLocation = "C:\sqlite\db\\"
desiredReferanceScore = input('What percentage of graph you want:')
country = input('Country Name:')
db = createDatabase.createCountrydb(country, databseLocation)
parties = ['PTI', 'JUIF', 'PMLN', 'PPP', 'JI']
seedsBasic = selectSeed(parties, db, 10)