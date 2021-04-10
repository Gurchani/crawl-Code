
from pandas import DataFrame
import pandas as pd
import createDatabase

def getCrawlCost(users, db):
    followerCount = []
    for i in users:
        query = 'select follower_count from userdetails where id = ' + str(i)
        for k in db.execute(query):
            followerCount.append(k[0])
    return followerCount

def getDataOfRetweetersFriends(party, db):
    Query = "Select * from " + party + "retweeterFriends"
    recoverall = db.execute(Query)
    df = DataFrame(recoverall.fetchall())
    df.columns = ['retweeterId', 'friend']
    return df

def createIN_OUTPopularityDF(parties, listOfFriendCounts, allUniqueFriends):
    print(len(listOfFriendCounts))
    friendFrequencyList = []
    for i in allUniqueFriends:
        emptyList = []
        for k in listOfFriendCounts:
            try:
                emptyList.append(k.loc[i])
            except:
                emptyList.append(0)
        friendFrequencyList.append(emptyList)
    columnNames = []
    for i in parties:
        columnNames.append(i)
    friendFrequencyDF = pd.DataFrame(friendFrequencyList, columns=columnNames ,index=allUniqueFriends)
    return friendFrequencyDF

def calculateRelativePopuarity(df):
    df['Total'] = 0
    colNames = df.columns
    for i in colNames:
        if i != 'Total' or i != 'crawlCost':
            df['Total'] = df['Total'] + df[i]
    for i in colNames:
        df[i + 'Rel'] = (df[i]* df[i])/(df['Total'] * df['crawlCost'])
    return df

def selectSeed(parties, db, NumberOfRetweeters):
    setOfAllFriends = set()
    listOfFriendCounts = []
    for i in parties:
        partyDf = getDataOfRetweetersFriends(i, db)
        FriendPopularityInsideParty = partyDf['friend'].value_counts()
        listOfFriendCounts.append(FriendPopularityInsideParty)
        popularFriends = set(partyDf['friend'])
        setOfAllFriends = setOfAllFriends.union(popularFriends)

    popularityDF = createIN_OUTPopularityDF(parties, listOfFriendCounts, list(setOfAllFriends))
    popularityDF['crawlCost'] = getCrawlCost(list(popularityDF.index), db)
    #print(popularityDF[popularityDF['PTI'] > 0].sort_values(by='PPP', ascending=False).head(15))
    relativePop = calculateRelativePopuarity(popularityDF)
    SeedValidationList = []
    for i in parties:
        print(i)

        textRel = i + 'Rel'
        print(relativePop.sort_values(by=textRel, ascending=False).head)
        SeedValidationList.append(relativePop.sort_values(by=textRel, ascending=False).index)
    return validateSeed(list(set(parties)), SeedValidationList, db, NumberOfRetweeters)

def validateSeed(parties, SeedLists, db, retweeterSetSize):
    print('Seed list')
    print(SeedLists)
    print('Parties')
    print(parties)
    print('  ')
    for i, party in zip(SeedLists, parties):
        createDatabase.createCoverTable(party, db)
        listOfFinalSeeds = []
        for j in i:
            listOfFinalSeeds.append(j)
            CoverQuery = 'Insert into ' +party+'covered Select retweeterId from ' + party + 'retweeterFriends where FriendId ='+ str(j) + ' and ' \
                                                                                                                                        'retweeterId not in (select retweeterId from '+party+'covered)'
            db.execute(CoverQuery)
            getSeeds = 'Select COUNT(*) from '+party+'covered'
            howManyDone = 0
            for k in db.execute(getSeeds):
                howManyDone = k[0]
            if howManyDone/retweeterSetSize > 0.99:
                print(listOfFinalSeeds)
                break

#Testing Code
#import createDatabase
#print('asdasd')
#databseLocation = "C:\sqlite\db\\"
#desiredReferanceScore = input('What percentage of graph you want:')
#country = input('Country Name:')
#db = createDatabase.createCountrydb(country, databseLocation)
#parties = ['FN', 'PTI']
#seedsBasic = selectSeed(parties, db, 50)
#validateSeed(parties, seedsBasic, db, 50)

