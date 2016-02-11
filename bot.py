#!/usr/bin/env python

import tweepy

#from our keys module (keys.py), import the keys dictionary
from keys import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

ALOT_HERD = (
    # the inner quotes are for searching the exact string
    # ('"exact string to search"', 'tweet response', 'tweet_image.png')
    ('"alot of bacon"', 'You just summoned Alot of bacon!', 'bacon.png'),
    ('"alot of beer"', 'You just summoned Alot of beer!', 'beer.png'),
    ('"like christmas alot"', 'I like it too! Alot of ho ho ho!', 'christmas.png'),
    ('"alot more dangerous"', 'Be careful! Alots sure are dangerous!', 'dangerous.png'),
    ('"alot of fire"', 'You just summoned Alot of fire!', 'fire.png'),
    ('"alot of mist"', 'You just summoned Alot of mist!', 'mist.png'),
    ('"alot of money"', 'You just summoned Alot of money!', 'money.png'),
    ('"I like this alot more"', 'That is so rude of you to say! All Alots are equally lovable', 'more.png'),
    ('"I am sad alot"', 'Alot confused, alot not understand feelings', 'sad.png'),
    ('"thanks alot"', 'You are welcome, fellow Alot lover!', 'thanks.png'),
)

for alot in ALOT_HERD:
    query = alot[0]

    tweet_list = api.search(q=query, count=20, lang="en")

    tweets_answered = 0

    for tweet in tweet_list:
        screen_name = tweet.user.screen_name

        # avoid retweets
        if (
            hasattr(tweet, 'retweeted_status') or
            'RT @' in tweet.text or
            api.me().screen_name == screen_name
        ):
            print "this is a retweet, let's try with the next one"

        else:
            message = ".@{username} {message}".format(
                username=screen_name,
                message=alot[1]
            )
            image_path = "media/{image_name}".format(image_name=alot[2])

            # if the tweet is a duplicate an exception is raised
            try:
                # follow the user
                api.create_friendship(screen_name)

                api.update_with_media(
                    filename=image_path,
                    status=message,
                    in_reply_to_status_id=tweet.id
                )

                tweets_answered += 1
                print '{tweets_answered} {query}'.format(
                    tweets_answered=tweets_answered,
                    query=query
                )

                print message

                if tweets_answered >= 2:
                    break

            except tweepy.TweepError as e:
                print e.message[0]['code']
                print e.args[0][0]['code']


