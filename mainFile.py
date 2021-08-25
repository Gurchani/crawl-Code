databseLocation = "E:\Twitter Country Data\\"
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
import mergeAllGraphs

db = createDatabase.createCountrydb(country, databseLocation) #Done
#TwitterConnection = connectToTwitter.connect2() #Done
#leaderNames, parties = getLeaderNames.getNames() #Done #Temporarily taken off for testing
leaderNames = ['sdriks', 'liberalerna', 'Centerpartiet', 'kdriks', 'vansterpartiet', 'miljopartiet', 'socialdemokrat', 'moderaterna']
parties = ['SD', 'L', 'C', 'KD', 'V', 'ML', 'S', 'M']
retweetersLimit = input('Retweeters Limit:')
#getTweets.getTweets(leaderNames, db) #Done
print("Tweets Collected")
#getRetweeters.getRetweeters(leaderNames, parties, db) #Done
print("Retweeters Collected")
#processRetweeters.process(leaderNames, parties, db) #Done
print("Retweeters Processed")
#crawlFriends.crawl(list(set(parties)), db, retweetersLimit) #Done
print("Friends Crawled")
SeedProfiles = seedSelection.selectSeed(list(set(parties)), db, retweetersLimit, 0.90, 50) #Done
print("Seeds Selected")
crawlFollowers.getFollowers(SeedProfiles, parties, db) #Tested Once
print("Followers Collected")
crawlFriends2ndTime.crawl(parties, db) #Tested Once
print("Friends Collected Second Time")
getProfileDetails.getAllProfilesAndDetails(parties, db) #Tested Once
print("Profiles Details Collected")
mergeAllGraphs.merge(country, parties, db) #Tested Once
print("All Graphs Merged")
print("Referance Score: " + calculateReferanceScore.score()) #Tested Only Once (few errors)



