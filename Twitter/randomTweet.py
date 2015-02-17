from twitter import *
import random

from twitter_app_credentials import *

twitter = Twitter(
auth=OAuth(access_token_key, access_token_secret, consumer_key, consumer_secret))
rawtimeline = twitter.statuses.user_timeline(screen_name="bashcookbook")
cleanup = ['RT','@']
status = []
for line in rawtimeline:
    tweet = ("%s: %s" % (line["user"]["screen_name"], line["text"]))
    if not any(cleanup in tweet for cleanup in cleanup):
        status.append(tweet)
status = (random.choice(status))
decoded = status.encode('utf-8')
msg = "^ @%s" % decoded
print msg
