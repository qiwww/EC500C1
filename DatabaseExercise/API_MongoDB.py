import twitter
import json
import urllib.request
import os
import subprocess
from google.cloud import videointelligence
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson

import pymongo
from pymongo import MongoClient
from bson import json_util
# Use default client which will defaults to the MongoDB instance 
# that runs on the localhost interface on port 27017
client = MongoClient()
db = client.tweetDB
tweetDB = db.tweetDB


############################################ Twitter ################################################
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

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


############################################ Twitter ################################################

from datetime import datetime
result = tweetDB.insert_one({"Author": "wallpapermag"})

if __name__ == "__main__":
	screen_name = "wallpapermag"
	Image_Number = 30
    get_images("wallpapermag")
    make_video()
    get_description()


cursor = tweetDB.find()
for ele in cursor:
    print(ele)


remove_all = tweetDB.delete_many({})
remove_all.deleted_count


tweetDB.drop()


    