
def getHighFrequencyRetweeters(party , database):
    Query = 'Create table IF NOT EXISTS '+party+'retweeterFreq as Select retweeterId, count(*) as freq from ' + party+'retweeters ' \
                                                                      'group by retweeterId'

    print(Query)
    database.execute(Query)

import getLeaderNames
def process(leaderNames, parties, database):
    partyLeaderDf = getLeaderNames.getLeaderPartyDF(leaderNames, parties,)
    parties = partyLeaderDf['party'].unique()
    for i in parties:
        getHighFrequencyRetweeters(i, database)