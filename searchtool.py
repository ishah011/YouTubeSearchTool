from flask import Flask
from flask import render_template, request, url_for, redirect
from apiclient import discovery
from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

app = Flask(__name__)

#!/usr/bin/python
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyB-bxt14EM4OME397miur95Wl94PVa3oT8"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

xrv = []
yrv = []

def youtubefunc(query, sort, rv):

	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
	
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
		rv.append(video["snippet"]["title"] + " :: " + video["snippet"]["channelTitle"])

@app.route('/', methods=['GET','POST'])
def index(xrv=xrv):
	if request.method == 'POST':
		query = request.form["search"]
		if request.form["xselection"] is "Ratings":
			xsort = "rating"
			xrv.append(1)
		elif request.form["xselection"] is "Views":
			xsort = "viewCount"
			xrv.append(2)
		elif request.form["xselection"] is "Year":
			xsort = "date"
			xrv.append(3)
		else:
			xsort = "rating"
			xrv.append(4)
		if request.form["yselection"] is "Ratings":
			ysort = "rating"
			yrv.append(1)
		elif request.form["yselection"] is "Views":
			ysort = "viewCount"
			yrv.append(2)
		elif request.form["yselection"] is "Year":
			ysort = "date"
			yrv.append(3)
		else:
			ysort = "rating"
			yrv.append(4)

		# youtubefunc(query, xsort, xrv)
		# youtubefunc(query, ysort, yrv)
		return redirect(url_for('result'))
	else:
		return render_template('search.html',xrv=xrv, yrv=yrv)

@app.route('/result', methods=['GET'])
def result(xrv=xrv, yrv=yrv):
	return render_template('result.html',xrv=xrv, yrv=yrv)