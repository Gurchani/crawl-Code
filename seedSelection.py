
from pandas import DataFrame
import pandas as pd
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
        df['Total'] = df['Total'] + df[i]
    for i in colNames:
        df[i + 'Rel'] = (df[i]* df[i])/df['Total']
    return df

def selectSeed(parties, db):
    setOfAllFriends = set()
    listOfFriendCounts = []
    for i in parties:
        partyDf = getDataOfRetweetersFriends(i, db)
        FriendPopularityInsideParty = partyDf['friend'].value_counts()
        listOfFriendCounts.append(FriendPopularityInsideParty)
        popularFriends = set(partyDf['friend'])
        setOfAllFriends = setOfAllFriends.union(popularFriends)

    popularityDF = createIN_OUTPopularityDF(parties, listOfFriendCounts, list(setOfAllFriends))
    #print(popularityDF[popularityDF['PTI'] > 0].sort_values(by='PPP', ascending=False).head(15))
    relativePop = calculateRelativePopuarity(popularityDF)
    print(relativePop.sort_values(by='PTIRel', ascending=False))
#Testing Code
#import createDatabase
#databseLocation = "C:\sqlite\db\\"
#desiredReferanceScore = input('What percentage of graph you want:')
#country = input('Country Name:')
#db = createDatabase.createCountrydb(country, databseLocation)
#selectSeed(['PTI', 'PMLN', 'PPP'], db)