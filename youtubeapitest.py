#!/usr/bin/python

from apiclient import discovery
from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyB-bxt14EM4OME397miur95Wl94PVa3oT8"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# Call the search.list method to retrieve results matching the specified
# query term.
search_response = youtube.search().list(
  q="puppy",
  part="snippet",
  maxResults=2,
  type="video"
).execute()

# search_response["items"][0]["snippet"]["title"]
for video in search_response["items"]:
  print video["snippet"]["title"] + " - " + video["snippet"]["channelTitle"]