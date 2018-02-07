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
import wget
import ffmpeg
import io
import os
import subprocess
from PIL import Image
from resizeimage import resizeimage
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Twitter API credentials
consumer_key = "Enter the consumer_key"
consumer_secret = "Enter the consumer_secret"
access_key = "Enter the access_key"
access_secret = "Enter the access_secret"


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

screen_name = input("Please Enter a Twitter account name")


def get_images(screen_name):
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    # Get the tweets from a user up to 200
    tweets = api.user_timeline(screen_name = screen_name,
                               count = 200, include_rts = False,
                               exclude_replies = True)
    
    # Obtain the full path for the images
    media_files = set()
    for status in tweets:
        media = status.entities.get('media', [])
        if(len(media) > 0):
            media_files.add(media[0]['media_url'])
            
    # Download images
    for media_file in media_files:
        wget.download(media_file)
    
    path = '/home/EC500/APIs/pictures/'
    # Rename Pictures 
    nameCount = 0
    for file in os.istdir(path):
        if file.endswith('jpg'):
            with open(file, 'r+b'):
                with Image.open(file) as image:
                    newPic = resizeimage.resize_cover(image, [2000,2000], validate = False)
                    newPic.save(file,image.format)
            os.rename(file, 'Pic'+ nameCount + '.jpg')
        elif filename.endswith('.png'):
            with open(file, 'r+b'):
                with Image.open(file) as image:
                    newPic = resizeimage.resize_cover(image, [2000,2000], validate = False)
                    newPic.save(file,image.format)
            os.rename(file, 'Pic'+ nameCount + '.png')
            
# make images to video
def make_video():
    subprocess.call()
    subprocess.call("ffmpeg -framerate 1 -i Pic%d.jpg output.mp4",shell=True)
    # ffmpeg -loop 1 -i [INPUT FILENAME] -c:a libfdk_aac -ar 44100 -ac 2 -vf "scale='if(gt(a,16/9),1280,-1)':'if(gt(a,16/9),-1,720)',                                  
    # pad=1280:720:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -b:v 10M -pix_fmt yuv420p -r 30 -shortest -avoid_negative_ts make_zero -fflags +genpts -t 1 OUTPUTFILENAME.mp4    
def get_discription():
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    
    pathDir =  os.listdir('/home/EC500/APIs/pictures/')
    
    f = open('')
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

try:
    get_images(screen_name)
    make_video()
    get_discription()
except:
    print "Error Occur, please try again"
    