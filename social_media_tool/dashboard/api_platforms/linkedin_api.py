import os
from dbm.sqlite3 import GET_SIZE

import requests
from certifi import contents
from urllib.parse import urlencode
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../../.env")

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")

LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", default=None)
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", default=None)
LINKEDIN_API_URL = "https://api.linkedin.com/v2"




def auth_linkedin():
    #1. Providing a link to login and authenticate
    params = {
        "response_type" : "code",
        "client_id" : LINKEDIN_CLIENT_ID,
        "redirect_uri" : LINKEDIN_REDIRECT_URI,
        "scope" : "openid profile w_member_social"
    }

    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"

    print("authentication url to be opened:")
    print(auth_url)

    #2. Getting an authorization code in response
    code = input("paste received authorization code here: ").strip()

    print("exchanging auth code for token...")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
    }

    #3. Requesting Access token with previously received Authorization token in body
    token_response = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken", data, headers={"Content-Type" : "application/x-www-form-urlencoded"}
    )

    print("token response:" + str(token_response.json()))

    #4. Receiving Access token
    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data['access_token']
        print("Received access token: " + access_token)
        return access_token
    else:
        print("GOT TOKEN RESPONSE ERROR")
        print("Status code: " + str(token_response.status_code))
        print("Response: " + str(token_response.json()))
        exit(1)




def post_linkedin(text, image_path=None):
    #1. Getting profile ID
    userinfo_response = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={
            "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}"
        }
    )

    print("Profile full response: " + str(userinfo_response.json()))

    profile_data = userinfo_response.json()
    profile_urn = profile_data.get("sub")

    if not profile_urn:
        print("Error: Could not get profile URN")
        print("Full response:", profile_data)
        return None

    #2. Prepaing post data
    post_data = {
        "author" : f"urn:li:person:{profile_urn}",
        "commentary" : text,
        "visibility" : "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    #3. Posting to LinkedIn
    post_response = requests.post(
        "https://api.linkedin.com/rest/posts",
        headers={
            "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
            "LinkedIn-Version": "202507",
            "Content-Type": "application/json"
        },
        json=post_data
    )

    if post_response.status_code == 201:
        print("Post created successfully")

        try:
            data = post_response.json() if post_response.text.strip() else {}
        except ValueError:

            data = {}

        return {
            "success": True,
            "id": data.get("sub"),
            "url": None,
            "message": "Post created successfully"
        }
    else:
        print(f"Error: {post_response.status_code}")
        print(post_response.text)
        return {
            "success": False,
            "error": "Failed to create post"
        }


if __name__ == "__main__":
    # access_token = auth_linkedin()
    post_linkedin("test text4")

