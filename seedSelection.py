
from pandas import DataFrame
import pandas as pd
import setHittingProblem
import createDatabase
import getProfileDetails

weightToexclusivity = 0.5

def getCrawlCost(users, db):
    #getProfileDetails.getProfileDetails(users,db ) #temp
    followerCount = []
    for i in users:
        query = 'select id, followers_count from userdetails where id = ' + str(i)
        for k in db.execute(query):
            #print(k[0])
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
    countx = 0
    for i in allUniqueFriends:
        countx = countx + 1
        b = countx / len(allUniqueFriends) * 100
        print(b, end="\r")
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

def calculateRelativePopuarity(df, parties):
    df['Total'] = 0
    colNames = df.columns
    for i in colNames:
        if i in parties:
            df['Total'] = df['Total'] + df[i]
    for i in colNames:
        if i in parties:
            #df[i + 'Rel'] = (df[i]* df[i])/(df['Total'] * df['crawlCost'])
            df[i + 'Rel'] = ((df[i] * df[i]) / (df['Total']))
    return df

def selectSeed(parties, db, NumberOfRetweeters, targetPercentage, numberOfFriendsToSelectFrom):
    setOfAllFriends = set()
    listOfFriendCounts = []
    partiesDF = []
    partySeeds = []
    for i in parties:
        partyDf = getDataOfRetweetersFriends(i, db)
        partiesDF.append(partyDf)
        FriendPopularityInsideParty = partyDf['friend'].value_counts()
        listOfFriendCounts.append(FriendPopularityInsideParty)
        popularFriends = set(partyDf['friend'])
        setOfAllFriends = setOfAllFriends.union(popularFriends)

    popularityDF = createIN_OUTPopularityDF(parties, listOfFriendCounts, list(setOfAllFriends))
    crawlCostDF = getCrawlCost(list(popularityDF.index), db)
    popularityDF = popularityDF.merge(crawlCostDF, left_index = True, right_on ='id', how='inner')
    #popularityDF['crawlCost'] =
    #print(popularityDF[popularityDF['PTI'] > 0].sort_values(by='PPP', ascending=False).head(15))
    relativePop = calculateRelativePopuarity(popularityDF, parties)
    SeedValidationList = []
    count = 0
    for i in parties:
        partyRTFriends = partiesDF[count]
        textRel = i + 'Rel'
        print(i)
        pd.set_option('display.max_columns', None)
        #print(relativePop.sort_values(by=textRel, ascending=False).head())
        partySeeds.append(list(relativePop.sort_values(by=textRel, ascending=False).head(numberOfFriendsToSelectFrom)['id'].values))
        count = count + 1
    # 24th September 2021    partySeeds.append(setHittingProblem.findTheBestCombo(relativePop.sort_values(by=textRel, ascending=False).head(numberOfFriendsToSelectFrom), textRel, partyRTFriends, NumberOfRetweeters, targetPercentage))

    #    SeedValidationList.append(relativePop.sort_values(by=textRel, ascending=False)['id'])
    #return validateSeed(list(set(parties)), SeedValidationList, db, NumberOfRetweeters)
    return partySeeds

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
                return

#Testing Code
#import createDatabase
#print('asdasd')
#databseLocation = "C:\sqlite\db\\"
#desiredReferanceScore = input('What percentage of graph you want:')
#country = input('Country Name:')
#db = createDatabase.createCountrydb(country, databseLocation)
#parties = ['PTI', 'JUIF', 'PMLN', 'PPP', 'JI']

#seedsBasic = selectSeed(parties, db, 50, 0.90, 5)
#print(seedsBasic)

