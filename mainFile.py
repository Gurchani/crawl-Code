databseLocation = "C:\sqlite\db\\"
desiredReferanceScore = input('What percentage of graph you want:')
country = input('Country Name:')

import  connectToTwitter
import getLeaderNames
import crawlFriends
import crawlFollowers
import  getTweets
import getRetweeters
import getProfileDetails
import calculateReferanceScore
import createDatabase
import  processRetweeters

db = createDatabase.createCountrydb(country, databseLocation) #Done
#TwitterConnection = connectToTwitter.connect2() #Done
leaderNames, parties = getLeaderNames.getNames() #Done
getTweets.getTweets(leaderNames, db) #Done
getRetweeters.getRetweeters(leaderNames, parties, db) #Done
processRetweeters.process(leaderNames, parties, db)
crawlFriends.crawl(credentials, databseLocation)
getSeedProfiles = ()
count = 0
while True:
    getProfileDetails(credentials, leaderNames, databseLocation)
    if count%2 == 0:
        crawlFriends.crawl(credentials, databseLocation)
    else:
        crawlFollowers.crawl(credentials, databseLocation)
    refScore = calculateReferanceScore.score()
    if refScore > desiredReferanceScore:
        break
print('Process is complete and your graph is ready')