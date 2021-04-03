
import oauth2 as oauth

def connect():
    CONSUMER_KEY = input('CONSUMER_KEY:')
    CONSUMER_SECRET = input('CONSUMER_SECRET:')
    ACCESS_KEY = input('ACCESS_KEY:')
    ACCESS_SECRET = input('ACCESS_SECRET:')


    return [CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET]

def connectToTwitter(credentials):
    consumer = oauth.Consumer(key=credentials[0], secret=credentials[1])
    access_token = oauth.Token(key=credentials[2], secret=credentials[3])
    client = oauth.Client(consumer, access_token)
    return client


def connect2():
    CONSUMER_KEY = input('CONSUMER_KEY:')
    CONSUMER_SECRET = input('CONSUMER_SECRET:')
    ACCESS_KEY = input('ACCESS_KEY:')
    ACCESS_SECRET = input('ACCESS_SECRET:')
    client = connectToTwitter([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET])
    return client