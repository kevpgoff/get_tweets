#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import time

import json
import tweepy
import schedule

consumer_key = "XXXXX"
consumer_secret = "XXXXX"
access_key = "XXXXX"
access_secret = "XXXXX"

def get_tweets(username):
	
	with open(keys.json) as json_file:
		json_data = json.load(json_file)
	
	for item in json_data["keys"]:
		if item["username"] == username:
			consumer_key = item["consumer_key"]
			consumer_secret = item["consumer_secret"]
			access_key = item["access_key"]
			access_secret = item["access_secret"]
	
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	number_of_tweets = 10

	tweets = api.user_timeline(screen_name = username,count = number_of_tweets)
	
	data = {}
	data['tweets'] = []
	
	for tweet in tweets:
		data['tweets'].append({
		'username': username,
		'id': tweet.id_str,
		'text': tweet.text.encode('utf-16', 'surrogatepass').decode('utf-16')
		})
		
	print ("writing to {0}_tweets.json".format(username))
	with open("{0}_tweets.json".format(username), 'w') as outfile:
		json.dump(data, outfile, sort_keys=True, indent=4)
		
def post_fb(username):
	with open(keys.json) as json_file:
		json_data = json.load(json_file)
	
	for item in json_data["keys"]:
		if item["username"] == username:
			ACCESS_TOKEN = item["access_token"]
			
	graph = facebook.GraphAPI(ACCESS_TOKEN)
	
	with open('{0}_tweets.json'.format(username)) as json_file:
		json_data = json.load(json_file)
	
	for item in json_data["tweets"]:
		with open('{0}_posted.txt'.format(username)) as postedfiles:
			if item["id"] not in postedfiles.read():
				if "t.co" not in item["text"]:
					graph.put_object("me", "feed", message=item["text"])				
			else:
				postedfiles.write(item["id"] + "\n")
					
if __name__ == '__main__':

    if len(sys.argv) == 2:
        schedule.every(30).minutes.do(get_tweets(sys.argv[1]))
		schedule.every().hour.do(post_fb(sys.argv[1])
		while True:
		schedule.run_pending()
		time.sleep(1)
    else:
        print ("Error: enter one username")

    #alternative method: loop through multiple users
	# users = ['user1','user2']

	# for user in users:
	# 	get_tweets(user)
