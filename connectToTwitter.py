
import oauth2 as oauth
import random
import authenticationDB

def connectToTwitter(credentials):
    consumer = oauth.Consumer(key=credentials[0], secret=credentials[1])
    access_token = oauth.Token(key=credentials[2], secret=credentials[3])
    client = oauth.Client(consumer, access_token)
    return client


#For me and for testing
def getNewAuthetication():
    return authenticationDB.Authentications()

#For me and for testing
def connect3():
    keys = getNewAuthetication()
    print(keys)
    client = connectToTwitter([keys[0], keys[1], keys[2], keys[3]])
    return client


#for release
def connect2():
    CONSUMER_KEY = input('CONSUMER_KEY:')
    CONSUMER_SECRET = input('CONSUMER_SECRET:')
    ACCESS_KEY = input('ACCESS_KEY:')
    ACCESS_SECRET = input('ACCESS_SECRET:')
    client = connectToTwitter([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET])
    return client