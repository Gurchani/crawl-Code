
def getHighFrequencyRetweeters(leaderName , database):
    Query = 'Create table IF NOT EXISTS '+leaderName+'retweeterFreq as Select retweeterId, count(*) as freq from ' + leaderName+'retweeters ' \
                                                                      'group by retweeterId order by freq desc'

    print(Query)
    database.execute(Query)

def process(leaderNames, database):
    for i in leaderNames:
        getHighFrequencyRetweeters(i, database)