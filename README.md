# Social Media Management App

A web application that allows users to upload images, write descriptions, and post simultaneously to multiple social media platforms, including **LinkedIn, Pinterest, Twitter, Facebook, and Instagram**.

---

## Features

- Upload images with descriptions.
- Post content simultaneously to multiple platforms.
- Easy configuration via environment variables.

---

## Prerequisites

Before running the application, you need to:

1. Set up developer apps on the following platforms to get the required credentials:

   - [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
   - [Pinterest Developers](https://developers.pinterest.com/)
   - [Twitter Developer Portal](https://developer.twitter.com/)
   - [Facebook for Developers](https://developers.facebook.com/)
   - [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)

2. Create a `.env` file in the root folder of the project with the following content:

```env
# LinkedIn credentials
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_ACCESS_TOKEN=
LINKEDIN_REDIRECT_URI=

# Pinterest credentials
PINTEREST_ACCESS_TOKEN=

# Twitter credentials
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
USERNAME=

# Facebook credentials
..

# Instagram credentials
..
```
---

## Installation & Running

Before running the project, follow these steps:

1. **Navigate to the project directory:**

```bash
cd /social_media_tool/social_media_tool
```
2. **Install the required dependencies:**
   
```bash
pip install -r requirements.txt
```

3. **Run the development server:**

```bash
python manage.py runserver
```

4. **Open your browser and go to:**

```bash
http://127.0.0.1:8000
```
