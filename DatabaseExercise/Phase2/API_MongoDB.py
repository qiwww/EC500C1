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
'''
reference: https://github.com/XintongHao/EC500_C1/tree/master/API_exercise
'''
def get_timeline_media_urls(screen_name, count=200, exclude_replies=True): 
    """Get list of jpg urls found in media associated with tweets from a specific twitter accounts timeline

    Args:
        screen_name (str): Twitter screen name associated with desired timeline

    Keyword Arguments (optional):
        count (int): Number of tweets to look through (capped at 200 per api limits). Default 200.
        exclude_replies (bool): Exclude media found in tweets where specified user only replied. Default: True

    Returns:
        list: All .jpg image urls found in the twitter feed, as strings. 

    """
    with open("keys.dat") as f:
        keys = f.read().split()
    try:
        api = twitter.Api(consumer_key= keys[0],
                    consumer_secret=keys[1],
                    access_token_key=keys[2],
                    access_token_secret=keys[3])
    except:
        raise InvalidCredentialsException("Invalid twitter credentials")

    try:
        res = api.GetUserTimeline(screen_name=screen_name, count=count, trim_user=True, exclude_replies=exclude_replies)
    except Exception as e:
        raise e
    images = []
    for tweet in res:
        js = tweet._json["entities"]
        if "media" in js.keys():
            for media in js["media"]:
                if media["media_url"][-3:] == "jpg":
                    images.append(media["media_url"])
    if len(images) == 0:
        raise InvalidMediaException("No valid media found for screen_name: " + screen_name)
    return images

    def urls_to_movie(images, output="output.mp4"):
    """Generate local mp4 file from a list of urls, with 1 sec per images

    Args:
        images (list): List of images to include in movie, as strings

    Keyword Arguments (optional):
        output: Ouput filename for video. Default: output.mp4

    Returns:
        str: Output filename used by ffmpeg, in event provided filename was in use

    """
    count = 0
    while os.path.isfile(output):
        output = output.split(".")[0] + "(" + str(count) + ")." + output.split(".")[1]
        count += 1

    for i in range(len(images)):
        try:
            urllib.request.urlretrieve(images[i], "tmp_{}.jpg".format(str(i).zfill(4)))
        except Exception as e:
            raise e

    for i in range(len(images)):
        try:
            os.system(('''ffmpeg -loop 1 -i tmp_{}.jpg -c:a libfdk_aac -ar 44100 -ac 2 -vf "scale='if(gt(a,16/9),1280,-1)':'if(gt(a,16/9),-1,720)', pad=1280:720:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -b:v 10M -pix_fmt yuv420p -r 30 -shortest -avoid_negative_ts make_zero -fflags +genpts -t 1 tmp_{}.mp4''').format(str(i).zfill(4) , str(i).zfill(4)))
        except Exception as e:
            raise e

    with open("tmp_files.txt", "w") as f:
        for i in range(len(images)):
            f.write("file 'tmp_{}.mp4'\n".format(str(i).zfill(4)))

    try:
        os.system("ffmpeg -f concat -i tmp_files.txt " + output)

    except Exception as e:
        raise e

    #cleanup temp files
    for i in range(len(images)):
        os.remove("tmp_{}.jpg".format(str(i).zfill(4)))
        os.remove("tmp_{}.mp4".format(str(i).zfill(4)))
    # os.remove("tmp_files.txt".format(str(i).zfill(4)))

    return output
def video_analysis(filename):
    """Generate list of labels for a specified mp4 file, using Google cloud ideo intelligence

    Ouput is of form: 
        [{start: 0, end: 1, labels: [("cat", .56), ("animal>dog", .2)]}]
        Each labels is broken up by (category > categy > ... > entity , confidence level)

    Args:
        filename (str): Filename of input .mp4 file

    Returns:
        list: list of segments and labels, sorted by start time of each shot

    """
    credentials = service_account.Credentials.from_service_account_file(
        'googe.dat')
    try:
        client = videointelligence.VideoIntelligenceServiceClient(
            credentials=credentials
        )
    except Exception as e:
        raise e

    try:
        with open(filename, "rb") as f:
            video_data = f.read()
    except Exception as e:
        raise e

    try:
        result = client.annotate_video(
            input_content=video_data,
            features=['LABEL_DETECTION'],
        ).result()
    except Exception as e:
        raise e

    return result
def get_twitter_media_analysis(screen_name, count=200, exclude_replies=True, output_name="output.mp4", delete_movie=True):
    """Generate list of labels from the video anaylsis of a specified users twitter timeline

    Ouput is of form: 
        [{start: 0, end: 1, labels: [("cat", .56), ("animal>dog", .2)]}]
        Each labels is broken up by (category > categy > ... > entity , confidence level)

    Args:
       screen_name (str): Twitter screenname associated with desired timeline

    Keyword Arguments (optional):
       count (int): Number of tweets to look through (capped at 200 per api limits). Default: 200
       exclude_replies (bool): Exclude media found in tweets where specified user only replied. Default: True
       output_name (str): Filename of input .mp4 file. Default: output.mp4
       delete_movie (bool): Specified whether or not to remove local file after analysis. Default: True

    Returns:
        list: list of segments and labels, sorted by start time of each shot

    """
    images = get_timeline_media_urls(screen_name, count, exclude_replies)
    output_filename_actual = urls_to_movie(images, output=output_name)
    result = video_analysis(output_filename_actual)
#     if delete_movie:
#         os.remove(output_name)

    analysis_json = json.loads(MessageToJson(result)) 
#     print(analysis_json)
    imgage_idx = 1
    for shot_label in analysis_json["annotationResults"][0]["shotLabelAnnotations"]:
        entity = [shot_label["entity"]["description"]]

        for segment in shot_label["segments"]:
            entity.append(segment["confidence"])

        result = tweetDB.insert_one(
            {
            "imageInfo": [{"imgage_idx":imgage_idx, "decription": entity[0], "confidence": entity[1]}         
            ]
            }
        )
        imgage_idx +=1
    
    return analysis_json
############################################ Twitter ################################################

from datetime import datetime
result = tweetDB.insert_one({"Author": "wallpapermag"})
'''
# my version
if __name__ == "__main__":
	screen_name = "wallpapermag"
	Image_Number = 30
    get_images("wallpapermag")
    make_video()
    get_description()
'''
if __name__ == "__main__":
    get_twitter_media_analysis("wallpapermag", count=30)


cursor = tweetDB.find()
for ele in cursor:
    print(ele)


remove_all = tweetDB.delete_many({})
remove_all.deleted_count


tweetDB.drop()


    