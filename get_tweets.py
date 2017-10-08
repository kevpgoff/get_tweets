#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import time
import mmap
import os
import subprocess
import urllib.request

import json
import twitter
import schedule
import facebook

from pymongo import MongoClient

from colorama import Fore

client = MongoClient()

def put_video(video_url, page_id, access_token, descriptioninput, titleinput):
	video_file_name=title
	local_video_file = {'file': open(video_url, 'rb')}
 	path = "{0}/videos".format(page_id)
	fb_url = "https://graph-video.facebook.com/{0}?access_token={1}".format(
			path, access_token)
	r = requests.post(fb_url, files=local_video_file, title = titleinput, description = descriptioninput) 
	if r.status_code == 200:
		j_res = r.json()
		facebook_video_id = j_res.get('id')
		print ("facebook_video_id = {0}".format(facebook_video_id))
	else:
		print ("Facebook upload error: {0}".format(r.text))

def print_error(err):
	print >>sys.stderr, Fore.RED + sys.argv[0] + ' error: ' + err + Fore.RESET
	sys.stderr.flush()
	
def get_tweets(username):
	
	with open('keys.json') as json_file:
		json_data = json.load(json_file)
	
	for item in json_data["keys"]:
		if item["username"] == username:
			api = twitter.Api(consumer_key = item["consumer_key"], consumer_secret = item["consumer_secret"], access_token_key = item["access_key"], access_token_secret = item["access_secret"])

	number_of_tweets = 4

	tweets = api.GetUserTimeline(screen_name = username,count = number_of_tweets, exclude_replies = "true")
	
	
	json_file.close()
	data = {}
	data['tweets'] = []
	
	for tweet in tweets:
		print(tweet.media)
		imagecount = 0
		image_url = ""
		hasimg = False
		hasvid = False
		hasmedia = False
		filetype = ""
		filepath = "./images/"

		if("None" in str(tweet.media)):
			hasmedia = False
		else:
			hasmedia = True

		if("animated_gif" in str(tweet.media)):
			hasvid = True
		
		if(hasmedia == True and len(tweet.media) > 1):
			filetype = ".jpg"
			hasimg = True
			for i in range(0, len(tweet.media)):
				image_url = tweet.media[i].media_url_https
				urllib.request.urlretrieve(image_url, ((filepath) + username + str(tweet.id) + "-" + str(imagecount) + filetype))
				imagecount += 1

		if(hasvid == True):
			filetype = ".mp4"
			image_url = tweet.media[0].video_info['variants'][0]['url']
			urllib.request.urlretrieve(image_url, (filepath) + username + str(tweet.id) + filetype)

		if(hasmedia == True and tweet.media[0].type == 'photo' and len(tweet.media) == 1):
			hasimg = True
			if('.png' in tweet.media[0].media_url_https):
				filetype = ".png"
			else:
				filetype = ".jpg"
				image_url = tweet.media[0].media_url_https
			urllib.request.urlretrieve(image_url, (filepath) + username + str(tweet.id) + filetype)

		data['tweets'].append({
		'username': username,
		'id': tweet.id,
		'text': tweet.text,
		'media' : [{
			'hasimg' : str(hasimg),
			'hasgif' : str(hasvid),
			'image_url' : image_url,
			'filetype' : filetype,
			'albumnum' : imagecount
		}]
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
		with open('{0}_posted.txt'.format(username), 'r+') as postedfiles:
			for line in postedfiles:
				if item["id"] in line:
					checker = True
			for file in glob.glob('./images/*'):
				if item["id"] in file:
					hasimg = True
					if ".gif" in file:
						hasgif = True
					albumcounter += 1

			if checker == False:
				postedfiles.write(item["id"] + "\n")
				
			postedfiles.close()

		if item["media"][0]["albumnum"] > 0 and hasimg == True and checker == False and hasgif == False and "@" not in item["text"] and "instagram" not in item["text"]:
			for i in range(0, item["media"][0]["albumnum"]):
				graph.put_photo(open("./images/" + username + "-" + item["id"] + "-" + i + item["media"][0]["filetype"]))

		if item["media"][0]["albumnum"] == 0 and hasimg == True and checker == False and hasgif == False and "@" not in item["text"] and "instagram" not in item["text"]:
			graph.put_photo(open('/home/kevin/Desktop/get_tweets/test/images/' + username + '-' + item['id'] + '.jpg', 'rb'), message = item["text"][0:item["text"].find("https://t.co")])
			print("IMAGE POSTED: " + username + "-" + item["id"] + ".jpg")

		elif hasimg == True and checker == False and hasgif == True and "@" not in item["text"] and "instagram" not in item["text"]:
			put_video("./images/" + username + "-" + item["id"] + ".mp4", pg_id, ACCESS_TOKEN, "test description", "test title", album_path = "me/albums/" + item["id"])

		elif hasimg == False and checker == False and "t.co" not in item["text"] and "@" not in item["text"] and "instagram" not in item["text"]:
			graph.put_wall_post(item["text"])	
		
					
def main():
	#args = parser.parse_args()
	#IF RUNNING FROM CMD
	
	if len(sys.argv) == 2:
	#	schedule.every(5).minutes.do(get_tweets, sys.argv[1])
	#	schedule.every(10).minutes.do(post_fb, sys.argv[1])
	#	while True:
	#		schedule.run_pending()
	#		time.sleep(1)	
			
		#above for scheduling, below for single run		
		
    #else:
    #    print ("Error: enter one username")
	
	#FOR MANUAL SINGLE RUN
		get_tweets(sys.argv[1])
		#post_fb(sys.argv[1])
	
	else:
		print ("Error: enter one username")	
		
    #alternative method: loop through multiple users
	# users = ['user1','user2']

	# for user in users:
	# 	get_tweets(user)						
					
if __name__ == '__main__':
	sys.exit(main())
