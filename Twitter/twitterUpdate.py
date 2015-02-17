from twitter import *
import re
from twitter_app_credentials import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

twitter = Twitter(
auth=OAuth(access_token_key, access_token_secret, consumer_key, consumer_secret))

## Enable this block for multiple users
twitter_userlist = ['victorbrca', 'MississaugaLUG']

for user in twitter_userlist:
	RawTweet = twitter.statuses.user_timeline(screen_name=user,count=1)[0]
	RawTweetDate = RawTweet['created_at']
	UTCRawTweetDate = re.sub(r'\+[0-9]{4}', 'UTC', RawTweetDate)
	TweetDateToTime = datetime.strptime(UTCRawTweetDate, '%a %b %d %H:%M:%S %Z %Y')
	TweetDate = TweetDateToTime.strftime('%Y-%b-%d %H:%M')
	CurrentTime = datetime.utcnow()
	diff = relativedelta(CurrentTime, TweetDateToTime)
	if (diff.days == 0 and diff.hours == 0 and diff.minutes < 5):
		if diff.minutes < 1:
			Ago = "%s seconds ago" % diff.seconds
		else:
			Ago = "%s minutes ago" % diff.minutes
		tweet = ("@%s: %s (%s)" % (RawTweet["user"]["screen_name"], RawTweet["text"], Ago))
		msg = tweet.encode('utf-8')
		print msg
	else:
		print "No tweets for %s in the past 5 minutes" % user