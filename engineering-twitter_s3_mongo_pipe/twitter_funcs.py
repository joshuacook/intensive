from twitter import TwitterStream
from twitter import OAuth
from utility import get_credentials

def collect_tweets(tweet_iterator, n=50):
    tweets = [next(tweet_iterator) for _ in range(n)]
    print('{} Tweets'.format(n), end=' | ')
    return tweets

def create_tweet_iterator():
    credentials = get_credentials()

    oauth = OAuth(credentials['twitter']['token'],
                  credentials['twitter']['token_secret'],
                  credentials['twitter']['consumer_key'],
                  credentials['twitter']['consumer_secret'])

    twitter_stream = TwitterStream(auth=oauth)
    tweet_iterator = twitter_stream.statuses.filter(locations=credentials['bounding_box'])
    print("Created Tweet Iterator.")
    return tweet_iterator
