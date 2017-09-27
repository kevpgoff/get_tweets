# get_tweets.py: Python Script to Download Tweets and Post to Facebook

Use this script to download the last 100 (or whatever number you choose) from any Twitter user and then post it to a Facebook wall or page.

## Installation & How To Use

```
$ git clone https://github.com/kevpgoff/get_tweets.git
$ cd get_tweets
```

Requires [Facebook-SDK](https://github.com/mobolic/facebook-sdk), [tweepy](https://github.com/tweepy/tweepy), and [Schedule](https://github.com/dbader/schedule)

Then you need to get your Twitter API Credentials by creating a new app at apps.twitter.com. Enter the appropriate API keys to the `keys.json` file. You also need to obtain a Facebook Access Token for either a user or an app. 

## Config

Add your keys for the users you wish to use the script on to a file called `keys.json` in the following format:
```
{
    "keys": [
        {
            "consumer_key": "XXXXX",
            "consumer_secret": "XXXXX",
            "access_key": "XXXXX",
	    "access_secret": "XXXXX",
	    "username": "XXXXX",
	    "access_token": "XXXXX"			
        }
    ]
}
```
`consumer_key` from apps.twitter.com

`consumer_secret`  from apps.twitter.com

`access_key`  from apps.twitter.com

`access_secret`  from apps.twitter.com

`username` Twitter Handle


`access_token` Facebook Access Token



Then you can run the script by entering one username at the command line: 

```
$ python
>>> get_tweets("[twitter_username]")
```
## To-Do

##### Short Term

* ~Controllable Scheduling~

* ~Image Support~

* GIF Support

* Fix Bugs

##### Long Term

* Implement in to Django app

* Migrate to Sqlite database


