
def getHighFrequencyRetweeters(leaderName , database):
    Query = 'Create table '+leaderName+'retweeterFreq Select retweeterId, count(*) as freq from ' + leaderName+'retweeters ' \
                                                                      'group by retweeterId order by freq desc'
    database.execute(Query)

def process(leaderNames, database):
    for i in leaderNames:
        getHighFrequencyRetweeters(i, database)