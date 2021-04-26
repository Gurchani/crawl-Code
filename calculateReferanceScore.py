import gc
import pandas as pd
import sqlite3

def score(country, db):
    query = 'select * from '+country+'completeGraph'
    cur = db.cursor()
    # db.execute(query)
    result = cur.execute(query).fetchall()
    #db.execute(query)
    #cols = [column[0] for column in query.description]
    results = pd.DataFrame.from_records(data=result, columns=['id', 'friend'])

    query2 = 'select id, friends_count, followers_count from userdetails'
    cur2 = db.cursor()
    result2 = cur2.execute(query2).fetchall()
    #db.execute(query2)
    #cols = [column[0] for column in result2.description]
    profileDetails = pd.DataFrame.from_records(data=result2, columns=['id','friends_count', 'followers_count'])
    return CalculateCombinedReferanceScores(results, profileDetails)


def CalculateCombinedReferanceScores(graphDF, profileDetails):
    profileDetails.set_index('id',inplace = True)
    frq = graphDF['id'].value_counts()
    freqFR = graphDF['friend'].value_counts()

    frq = frq.to_frame('foundFriends')
    freqFR = freqFR.to_frame('foundFollowers')

    frCombo = pd.concat([frq, freqFR], axis=1)
    frCombo.fillna(0, inplace=True)

    del freqFR
    del frq
    del graphDF
    gc.collect()

    incldCount = pd.merge(profileDetails[['friends_count', 'followers_count']], frCombo, left_index=True,
                          right_index=True)
    print(incldCount.shape)
    print(incldCount.sort_values(by=['foundFollowers'], ascending=False))
    print(incldCount.head())
    print(' ')

    del frCombo
    gc.collect()
    incldCount['referance'] = round((incldCount['foundFriends'] + incldCount['foundFollowers'] + 1) / (
                incldCount['friends_count'] + incldCount['followers_count'] + 1), 3)
    referanceScore = incldCount[(incldCount['referance'] >= 0.000001) & (incldCount['referance'] <= 1)][
        'referance'].mean()
    calculationBasis = incldCount[(incldCount['referance'] >= 0.000001) & (incldCount['referance'] <= 1)][
        'referance'].shape

    del incldCount
    gc.collect()
    return (referanceScore, calculationBasis[0])

#import createDatabase
#databseLocation = "C:\sqlite\db\\"
#desiredReferanceScore = input('What percentage of graph you want:')
#country = input('Country Name:')
#db = createDatabase.createCountrydb(country, databseLocation)
#print(score('Pakistan', db))