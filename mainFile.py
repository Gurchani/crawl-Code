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
import seedSelection
import crawlFriends2ndTime


db = createDatabase.createCountrydb(country, databseLocation) #Done
#TwitterConnection = connectToTwitter.connect2() #Done
leaderNames, parties = getLeaderNames.getNames() #Done
retweetersLimit = input('Retweeters Limit:')
getTweets.getTweets(leaderNames, db) #Done
getRetweeters.getRetweeters(leaderNames, parties, db) #Done
processRetweeters.process(leaderNames, parties, db) #Done
crawlFriends.crawl(list(set(parties)), db, retweetersLimit) #Done
SeedProfiles = seedSelection.selectSeed(list(set(parties)), db, retweetersLimit) #Done
crawlFollowers.getFollowers(SeedProfiles, parties, db) #Untested
crawlFriends2ndTime.crawl(parties, db) #Untested

#Not written yet
getProfileDetails.getProfileDetails()
calculateReferanceScore.score()
runExperiments()

