"""
Local gigs script:
	1. Find all gigs on SongKick in a locale for the next two weeks
	2. Login in to a given Spotify account
	3. Generate 2 playlists, one for today and one for the next two weeks
	4. Update every 24hrs
"""
from urllib.request import urlretrieve
import xml.etree.ElementTree as ET
import os
import datetime as dt
import spotipy

# set wd to songkick folder
os.chdir("C:\\Users\\dpj\\Documents\\python\\songkick")

# api key and metro id
api_key = ""
metro_id = "24571"
filename = "songkick.xml"

def get_songkick(api_key, metro_id, filename):
	"use songkick api to get xml calender for metro area"
	# http://api.songkick.com/api/3.0/metro_areas/{metro_area_id}/calendar.xml?apikey={your_api_key}
	urlretrieve("http://api.songkick.com/api/3.0/metro_areas/" + metro_id + "/calendar.xml?apikey=" + api_key, \
	filename)
	
def band_parse(filename, day_delta):
	tree = ET.parse(filename)
	root = tree.getroot()
	
	date_today = dt.datetime.now()
	date_future = date_today + dt.timedelta(days = day_delta)
	
	nx_two_days = []
	nx_two_weeks = []
	
	for event in root.iter('event'):
		for start in event.iter('start'):
			start = dt.datetime.strptime(start.get('date'), '%Y-%m-%d')
		for artist in event.iter('artist'):
			artist = artist.get('displayName')
			
			if start < date_future:
				nx_two_weeks.append(artist)
				
				if start < date_today + dt.timedelta(days=2):
					nx_two_days.append(artist)
	
	os.remove(filename)
	return((nx_two_days, nx_two_weeks))

def artist_uri(artists):
	artist_uri = {}
	
	spotify = spotipy.Spotify()
	
	for artist in artists:
		results = 
		
		