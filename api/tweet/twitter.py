import os
import tweepy
from tweepy.api import API
from time import localtime, strftime

auth = tweepy.OAuthHandler("Key1", "Key2")
auth.set_access_token("Key", "Key")
api = API(auth)

class Tweet():


    def __init__(self, tweet_media, model):
        """Initializes a tweet with a media, a text and reply_id"""
        self.text = "Image generated from model {} at #devmerge hackathon on {} by Team Vangogh".format(model,strftime("%a, %d %b %Y %H:%M:%S ", localtime()))
        self.media = tweet_media


    def post_to_twitter(self):

        status = api.update_with_media(filename=self.media,
                                       status=self.text)
        return status.id
