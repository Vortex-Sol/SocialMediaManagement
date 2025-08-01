import os

import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
username = os.getenv("USERNAME")

auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

def post_tweet(text, image_path=None):

    url = "https://api.twitter.com/2/tweets"
    payload = {"text": text}

    if image_path:
        upload_url = "https://upload.twitter.com/1.1/media/upload.json"
        try:
            with open(image_path, 'rb') as image_file:
                files = {'media': image_file}
                response = requests.post(upload_url, files=files, auth=auth)
                response.raise_for_status()
                media_id = response.json()['media_id_string']
                payload["media"] = {"media_ids": [media_id]}
        except FileNotFoundError:
            raise Exception(f"Image file not found: {image_path}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error uploading image: {str(e)}")

    response = requests.post(url, json=payload, auth=auth)
    if response.status_code == 201:
        data     = response.json().get('data', {})
        tweet_id = data.get('id')
        tweet_url = f"https://x.com/{username}/status/{tweet_id}"
        print("Tweet posted successfully!")
        print(data)
        print("Link to tweet:", tweet_url)

        return True, tweet_id, tweet_url
    else:
        print(f"Error posting tweet: {response.status_code}")
        print(response.text)
        return False, None, None