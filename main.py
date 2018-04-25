import tweepy
import config as cfg
from datadog import initialize as datadog_initialize
from datadog import api as datadog_api
from datadog import statsd

# Put keywords that you want to filter in an array.
# NOTE: Please see README for usage details
keywords = ['toronto raptors']

# Reading Configuration File
consumer_key = cfg.twitter_consumer_key
consumer_secret = cfg.twitter_consumer_secret
access_token = cfg.twitter_access_key
access_token_secret = cfg.twitter_access_secret
datadog_api_key = cfg.datadog_api_key

# Configuring Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)

# Configuring DataDog API
datadog_options = {
    'api_key': datadog_api_key
}
datadog_initialize(**datadog_options)

# Tweepy Stream
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
        for keyword in keywords:
            words = keyword.split(' ')
            for word in words:
                if word.lower() in status.text.lower():
                    statsd.increment( keyword + " tweet_count")
                    print("keyword: " + keyword)
                    break

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = twitter_api.auth, listener = myStreamListener)

myStream.filter(track=keywords)
