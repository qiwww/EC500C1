# -*- coding: utf-8 -*-
"""
Author: Qi Wang
Professor: Osama
Course: EC500 C1
Description: A library that downloads images from a twitter feed,
                convert them to a video,
                and describe the content of the images in the video.

"""

import tweepy #https://github.com/tweepy/tweepy
import json
import ffmpeg
import wget
import urllib.request
import io
import os
import subprocess
import sys
from PIL import Image
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Twitter API credentials
consumer_key = "X"
consumer_secret = "X"
access_key = "X"
access_secret = "X"


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


# Reference: 
    # https://miguelmalvarez.com/2015/03/03/download-the-pictures-from-a-twitter-feed-using-python/
def get_images(screen_name):
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    # Get the tweets from a user up to 200
    tweets = api.user_timeline(screen_name = screen_name,
                               count = 200, include_rts = False,
                               exclude_replies = True)
    
    last_id = tweets[-1].id
    while (True):
        more_tweets = api.user_timeline(screen_name = screen_name,
                                       count = 200,
                                       include_rts = False,
                                       exclude_replies = True,
                                       max_id = last_id - 1)
        # If there are no more tweets
        if (len(more_tweets) == 0):
            break
        else:
            last_id = more_tweets[-1].id - 1
            tweets = tweets + more_tweets
        
    # Obtain the full path for the images
    media_files = set()
    for status in tweets:
        media = status.entities.get('media', [])
        if(len(media) > 0):
            media_files.add(media[0]['media_url'])
    
    # Error Control
    if (len(media_files) == 0):
        print("User current doesn't have any picture.")
        sys.exit()
            
            
    # Download at most Image_Number images
    count = 0

    f = open('pictures_urls.txt', 'w')
    for media_file in media_files:
        wget.download(media_file,'image'+str(count)+media_file[-4:])
        f.write(media_file)
        count += 1
        if count == Image_Number:
            break
    
# make images to video
def make_video():
    try: 
        subprocess.call("ffmpeg -y -framerate 2  -i image%d.jpg outputvideo.mp4" )
    except (RuntimeError, TypeError,NameError):
        print ("Could not create video for ffmpeg issues")
        pass
    else:
        print ("")
def get_description():
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    
    pathDir =  os.path
    print(pathDir)
    f = open('pictures_discription.txt', 'w')
    # Loads the image into memory
    for file in pathDir:
        if file.endswith('jpg') or file.endswith('png'):
            with io.open(file,'rb') as image_file:
                content = image_file.read()
            image = types.Image(content=content)
            # Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations
    
            print('Labels:')
            f.write("Labels:"+"\n")    
    
    
            for label in labels:
                print(label.description)
    
                f.write(label.description+"\n")
    f.close()

if __name__ == '__main__':
    '''
    Get account name and number of pictures from user
    '''
    screen_name = input("Please Enter a Twitter Account Name  ")
    while (screen_name == ''):
        screen_name = input("Please Enter a Twitter Account Name  ")
    Image_Number = input("Please Enter How Many Pictures You Want to Display ")
    if Image_Number == '':
        Image_Number = 20 # Default
    else:   
        Image_Number = int(Image_Number)
        while (Image_Number < 0):
            Image_Number = input("Please Enter Pictures Number, Must Be A Positive Integer ")
            Image_Number = int(Image_Number)
    urls = []
    
    try:
        get_images(screen_name)
        print("Finish Downloading Pictures")
        get_description()
        print("Finish Getting Description")
        make_video()
        print("Finish Making Video")
    except:
        print("Error!")
    
