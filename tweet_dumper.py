#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import re

#Twitter API credentials
# consumer_key = ""
# consumer_secret = ""
# access_key = ""
# access_secret = ""

keys = [consumer_key,consumer_secret,access_key,access_secret]

def get_all_tweets(screen_name,keys=keys,filter=True):
	"""
	Get all tweets from @screen_name profile and write them on a txt file.
	Leave filter=True to remove RTs, links and mentions.
	Twitter only allows access to a users most recent 3240 tweets with this method.

	keys = [consumer_key,consumer_secret,access_key,access_secret]
	"""
	
	consumer_key,consumer_secret,access_key,access_secret = keys

	#re
	rt = r'^RT'
	link = r'https?:\/\/([\w\.-]+)\/([\w\.-]+)'
	mention = r'^\@'

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200,tweet_mode='extended')
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before {}".format(oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest,tweet_mode='extended')
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...{} tweets downloaded so far".format(len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	if filter: 
		outtweets = [tweet.full_text for tweet in alltweets if not re.match(rt, tweet.full_text) and not re.match(mention, tweet.full_text)]
		preproc = [re.sub(link, "", tweet)+"\n" for tweet in outtweets][::-1]
	else: 
		outtweets = [tweet.full_text for tweet in alltweets]
	
	#write the csv	
	with open('tweets/{}_tweets.txt'.format(screen_name), 'w', encoding='utf-8') as f:
		f.writelines(preproc)
		print('tweets/{}_tweets.txt was successfully created.'.format(screen_name))
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("jairbolsonaro")