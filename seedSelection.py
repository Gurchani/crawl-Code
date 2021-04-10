
from pandas import DataFrame
import pandas as pd
import createDatabase
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
        df[i + 'Rel'] = (df[i]* df[i])/(df['Total'] + df['crawlCost'])
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
    crawlCostDF = getCrawlCost(list(popularityDF.index), db)
    popularityDF = popularityDF.merge(crawlCostDF, left_index = True, right_on ='id', how='inner')
    #popularityDF['crawlCost'] =
    #print(popularityDF[popularityDF['PTI'] > 0].sort_values(by='PPP', ascending=False).head(15))
    relativePop = calculateRelativePopuarity(popularityDF)
    SeedValidationList = []
    for i in parties:
        textRel = i + 'Rel'
        print(relativePop.sort_values(by=textRel, ascending=False).head())
        SeedValidationList.append(relativePop.sort_values(by=textRel, ascending=False)['id'])
    return validateSeed(list(set(parties)), SeedValidationList, db, NumberOfRetweeters)

def validateSeed(parties, SeedLists, db, retweeterSetSize):
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
            if howManyDone/retweeterSetSize > 0.95:
                print(listOfFinalSeeds)
                break

#Testing Code
import createDatabase
print('asdasd')
databseLocation = "C:\sqlite\db\\"
desiredReferanceScore = input('What percentage of graph you want:')
country = input('Country Name:')
db = createDatabase.createCountrydb(country, databseLocation)
parties = ['PTI', 'JUIF']
seedsBasic = selectSeed(parties, db, 10)
validateSeed(parties, seedsBasic, db, 10)

