#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import time
import mmap
import os
import subprocess
import urllib.request
import glob

import json
import tweepy
import schedule
import argparse
import facebook
import magic

from colorama import Fore

consumer_key = "XXXXX"
consumer_secret = "XXXXX"
access_key = "XXXXX"
access_secret = "XXXXX"

parser = argparse.ArgumentParser(description="Scrape tweets")
parser.add_argument('--username', type=str, required = True)
parser.add_argument('--num', help='The number of tweets that will be scraped at each runtime', type=int, default=1, required = True)
parser.add_argument('--fb-mins', help='Number of minutes between posting loaded tweets to Facebook', type=int, default=60, required = True)
parser.add_argument('--twitter-mins', help='Number of minutes between tweet scrapes', type=int, default=60, required = True)

def print_error(err):
	print >>sys.stderr, Fore.RED + sys.argv[0] + ' error: ' + err + Fore.RESET
	sys.stderr.flush()
	
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

	number_of_tweets = 3

	tweets = api.user_timeline(screen_name = username,count = number_of_tweets, include_entities = True)
	
	
	json_file.close()
	data = {}
	data['tweets'] = []
	
	for tweet in tweets:
		data['tweets'].append({
		'username': username,
		'id': tweet.id_str,
		'text': tweet.text.encode('utf-16', 'surrogatepass').decode('utf-16'),
		'media' : [{
			'hasimg' : False,
			'numimages' : 0,
			'filtype' : ".jpg"
		}]
		})

	for status in tweets:
		if 'media' in status.entities:
			count = 0;
			for media in status.entities['media']:
				count += 1
				if media['type'] == 'photo':
					image_uri = media['media_url'] + ':large'
					filename = username + '-' + status.id_str
					filepath = './images/' + filename
					# download image
					urllib.request.urlretrieve(image_uri, filepath)
					# identify mime type and attach extension
					if os.path.exists(filepath):
						mime = magic.from_file(filepath, mime=True)
						if mime == "image/gif":
							newfilepath = filepath + ".gif"
						elif mime == "image/jpeg":
							newfilepath = filepath + ".jpg"
						elif mime == "image/png":
							newfilepath = filepath + ".png"
						else:
							err = filepath + ": unrecgonized image type"
							print_error(err)
							continue
						os.rename(filepath, newfilepath)
		
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
			pg_id = item["page_id"]
			json_file.close()
	#if facebook wall
	graph = facebook.GraphAPI(ACCESS_TOKEN)
	
	#graph = facebook.GraphAPI(ACCESS_TOKEN)
	#resp = graph.get_object('me/accounts')
	#page_access_token = None
	#for page in resp['data']:
	#	if page['id'] == pg_id:
	#		page_access_token = page['access_token']
	#graph = facebook.GraphAPI(page_access_token)
	
	with open('{0}_tweets.json'.format(username), 'r+') as json_file:
		json_data = json.load(json_file)

	for item in json_data["tweets"]:
		hasimg = False
		checker = False
		hasgif = False
		albumcounter = 0
		with open('{0}_posted.txt'.format(username), 'r+') as postedfiles:
			for line in postedfiles:
				if item["id"] in line:
					checker = True
			for file in glob.glob('./images/*'):
				if item["id"] in file:
					hasimg = True
					if ".gif" in file:
						hasgif = True
					albumcounter +=1

			if checker == False:
				postedfiles.write(item["id"] + "\n")
				
			postedfiles.close()
		if hasimg == True and checker == False and hasgif == False and "@" not in item["text"] and "instagram" not in item["text"]:
			graph.put_photo(open('/home/kevin/Desktop/get_tweets/test/images/' + username + '-' + item['id'] + '.jpg', 'rb'), message = item["text"][0:item["text"].find("https://t.co")])
			print("IMAGE POSTED: " + username + "-" + item["id"] + '.jpg')
		elif hasimg == True and checker == False and hasgif == True and "@" not in item["text"] and "instagram" not in item["text"]:
			print("GIF FOUND: Not posting anything.")
		elif hasimg == False and checker == False and "t.co" not in item["text"] and "@" not in item["text"] and "instagram" not in item["text"]:
			graph.put_wall_post(item["text"])	
		
					
def main():
	#args = parser.parse_args()
	#IF RUNNING FROM CMD
	
	if len(sys.argv) == 2:
		schedule.every(3).minutes.do(get_tweets, sys.argv[1])
		schedule.every(5).minutes.do(post_fb, sys.argv[1])
		while True:
			schedule.run_pending()
			time.sleep(1)	
			
		#above for scheduling, below for single run		
		
    #else:
    #    print ("Error: enter one username")
	
	#FOR MANUAL SINGLE RUN
	#	get_tweets(sys.argv[1])
	#	post_fb(sys.argv[1])
	
	else:
		print ("Error: enter one username")	
		
    #alternative method: loop through multiple users
	# users = ['user1','user2']

	# for user in users:
	# 	get_tweets(user)						
					
if __name__ == '__main__':
	sys.exit(main()) 탈
