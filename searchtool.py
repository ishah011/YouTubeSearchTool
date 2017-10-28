from __future__ import division
from flask import Flask
from flask import render_template, request, url_for, redirect
from apiclient import discovery
from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls

# set FLASK_APP = searchtool.py
#python -m flask run

app = Flask(__name__)

#!/usr/bin/python
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyB-bxt14EM4OME397miur95Wl94PVa3oT8"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

PLOTLY_USERNAME = 'ishah011'
PLOTLY_API_KEY = 'c1DyyepqDVUbvTIDfkqK'

plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)

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
	# for video in search_rating_response["items"]:
	# 	values = []
	# 	values.append("https://www.youtube.com/watch?v="+video["id"]["videoId"])
	# 	values.append(video["snippet"]["title"] + ' :: ' + video["snippet"]["channelTitle"])
	# 	rv.append(values)
	id_list = []
	for video in search_rating_response["items"]:
		id_list.append(video["id"]["videoId"])
	
	for video_id in id_list:
		video_lookup = youtube.videos().list(
			part='statistics',
			id=video_id
		).execute()
		for video in video_lookup["items"]:
			#likeCount, dislikeCount, viewCount
			#need to figure out how to get the year uploaded
			if sort == "rating":
				likes = int(video['statistics']['likeCount'])
				dislikes = int(video['statistics']['dislikeCount'])
				rating = (likes/(likes+dislikes))*100
				rv.append(rating) 
			elif sort == "viewCount":
				rv.append(int(video['statistics']['viewCount']))
			else:
				return render_template('search.html',xrv=xrv, yrv=yrv, error="Error retrieving stats")


@app.route('/', methods=['GET','POST'])
def index(xrv=xrv,yrv=yrv):
	error = ""
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

		return render_template('search.html',xrv=xrv, yrv=yrv, error=error)

@app.route('/result', methods=['GET'])
def result(xrv=xrv, yrv=yrv):
	data = [go.Scatter(
			x= xrv,
			y= yrv
		)] #this data actually contains titles and channels, not the views/ratings/year uploaded, which is what we want for the scatter plot
	layout = go.Layout(
		title='Results',
	)
	fig = go.Figure(data=data, layout=layout)
	result = tls.get_embed(py.plot(fig, filename='results', fileopt = 'overwrite'))
	return render_template('result.html',result=result)
	#return render_template('result.html', result=xrv)