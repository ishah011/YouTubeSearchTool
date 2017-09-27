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
		values = []
		values.append("https://www.youtube.com/watch?v="+video["id"]["videoId"])
		values.append(video["snippet"]["title"] + ' :: ' + video["snippet"]["channelTitle"])
		rv.append(values)

@app.route('/', methods=['GET','POST'])
def index(xrv=xrv,yrv=yrv):
	if request.method == 'POST':
		query = request.form["search"]
		xval = request.form["xselection"].encode("ascii")
		yval = request.form["yselection"].encode("ascii")
		if xval == "Ratings":
			xsort = "rating"
		elif xval == "Views":
			xsort = "viewCount"
		elif xval == "Year":
			xsort = "date"
		else:
			xsort = "rating"

		if yval == "Ratings":
			ysort = "rating"
		elif yval == "Views":
			ysort = "viewCount"
		elif yval == "Year":
			ysort = "date"
		else:
			ysort = "rating"

		youtubefunc(query, xsort, xrv)
		youtubefunc(query, ysort, yrv)

		return redirect(url_for('result'))
	else:
		del yrv[:]
		del xrv[:]

		return render_template('search.html',xrv=xrv, yrv=yrv)

@app.route('/result', methods=['GET'])
def result(xrv=xrv, yrv=yrv):

	return render_template('result.html',xrv=xrv, yrv=yrv)