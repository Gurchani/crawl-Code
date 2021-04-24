import gc
import pandas as pd
import sqlite3

def score(country, db):
    query = 'select * from '+country+'completeGraph'
    db.execute(query)
    #cols = [column[0] for column in query.description]
    results = pd.DataFrame.from_records(data=query.fetchall(), columns=['id', 'friend'])

    query2 = 'select * from userdetails'
    db.execute(query2)
    cols = [column[0] for column in query2.description]
    profileDetails = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    return CalculateCombinedReferanceScores(results, profileDetails)


def CalculateCombinedReferanceScores(graphDF, profileDetails):
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