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

query = raw_input('What would you like to search for?')
sorting = raw_input('What would you like to sort the results by, rating, views, or year uploaded?')

if(sorting == 'rating'):
	sort = "rating"
elif(sorting == 'views'):
	sort = "viewCount"
elif(sorting == 'year uploaded'):
	sort = "date"
else:
	print "The input is not rating, views, or year uploaded. Input is case-sensitive. Using default value of rating."
	sort = "rating"

# Call the search.list method to retrieve results matching the specified
# query term.
search_rating_response = youtube.search().list(
  q= query,
  part="snippet",
  maxResults=5,
  type="video",
  order= sort
).execute()

# search_response["items"][0]["snippet"]["title"]
for video in search_rating_response["items"]:
	print video["snippet"]["title"] + " :: " + video["snippet"]["channelTitle"]