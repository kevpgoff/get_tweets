#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import time
import mmap

import json
import tweepy
import schedule
import argparse
import facebook

consumer_key = "XXXXX"
consumer_secret = "XXXXX"
access_key = "XXXXX"
access_secret = "XXXXX"

parser = argparse.ArgumentParser(description="Scrape tweets")
parser.add_argument('--username', type=str, required = True)
parser.add_argument('--num', help='The number of tweets that will be scraped at each runtime', type=int, default=1, required = True)
parser.add_argument('--fb-mins', help='Number of minutes between posting loaded tweets to Facebook', type=int, default=60, required = True)
parser.add_argument('--twitter-mins', help='Number of minutes between tweet scrapes', type=int, default=60, required = True)


def get_tweets(username):
	
	with open('keys.json') as json_file:
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

	number_of_tweets = 15

	tweets = api.user_timeline(screen_name = username,count = number_of_tweets)
	
	
	json_file.close()
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
		outfile.close()
		
def post_fb(username):
	ACCESS_TOKEN = ""
	with open('keys.json') as json_file:
		json_data = json.load(json_file)
	
	for item in json_data["keys"]:
		if item["username"] == username:
			ACCESS_TOKEN = item["access_token"]
			json_file.close()
	graph = facebook.GraphAPI(ACCESS_TOKEN)
	
	with open('{0}_tweets.json'.format(username)) as json_file:
		json_data = json.load(json_file)
		json_file.close()
	
	for item in json_data["tweets"]:
		checker = False
		with open('{0}_posted.txt'.format(username), 'r+') as postedfiles:
			for line in postedfiles:
				if item["id"] in line:
					checker = True
					
			if checker == False:
				postedfiles.write(item["id"] + "\n")
				
			postedfiles.close()
			
		if checker == False and "t.co" not in item["text"]:
			graph.put_wall_post(item["text"])				
				
					
def main():
	#args = parser.parse_args()
	#IF RUNNING FROM CMD
    #if len(sys.argv) == 2:
    #   schedule.every(twitter-mins).minutes.do(get_tweets(sys.argv[1]))
	#	schedule.every(fb-mins).minutes.do(post_fb(sys.argv[1])
	#	while True:
	#	schedule.run_pending()
	#	time.sleep(1)
		
		#above for scheduling, below for single run
		
		#get_tweets(sys.argv[1])		
    #else:
    #    print ("Error: enter one username")
	
	if len(sys.argv) == 2:
		get_tweets(sys.argv[1])
		post_fb(sys.argv[1])
	else:
		print ("Error: enter one username")	
    #alternative method: loop through multiple users
	# users = ['user1','user2']

	# for user in users:
	# 	get_tweets(user)						
					
if __name__ == '__main__':
	sys.exit(main())
