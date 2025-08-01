import tweepy
import os
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

tweet_text = "hello world"

image_path = 'image.jpg'

alt_text = 's;aofjnvdsofjvnoseofjvn'

try:
    media = api.media_upload(image_path)
    api.create_media_metadata(media.media_id, alt_text)

    api.update_status(status=tweet_text, media_ids=[media.media_id])
    print("Tweet posted with image and alt text")

except Exception as e:
    print("Error posting tweet:", e)
