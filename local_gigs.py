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
	
def band_parse(filename, day_delta, coming_days):
	tree = ET.parse(filename)
	root = tree.getroot()
	
	date_today = dt.datetime.now()
	date_future = date_today + dt.timedelta(days = day_delta)
	
	artist_dict = {}
	
	for event in root.iter('event'):
		for start in event.iter('start'):
			start = dt.datetime.strptime(start.get('date'), '%Y-%m-%d')
		for artist in event.iter('artist'):
			artist = artist.get('displayName')
			
			if start < date_future:
								
				if start < date_today + dt.timedelta(days=coming_days):
					artist_dict.update({artist:0})
				else:
					artist_dict.update({artist:1})					
	
	os.remove(filename)
	return(artist_dict)

def artist_uri(artists):
	artist = list(artists)
	artist_uri = {}
	
	spotify = spotipy.Spotify()
	
	for artist in artists:
		results = spotify.search(q='artist:'+artist, type='artist', limit=1)
		
		if len(results['artists']['items']) != 0:
			results = results['artists']['items'][0]
			if results['name'] == artist:
				artist_uri.update({artist:results['uri']})
		
	return(artist_uri)	


def top_tracks(artist, uri, n_tracks):
	
	track_dict = {}

	for key, value in uri.items():
		results = spotify.artist_top_tracks(value)
		
		results = results['tracks']
		
		if(len(results) < n_tracks):
			for tracks in results:
				track_dict.update({tracks['uri']:artist[key]})
		else:
			for tracks in results[:n_tracks]:
				track_dict.update({tracks['uri']:artist[key]})
		
	return(track_dict)

def update_playlist(token, top_tracks, small_playlist, large_playlist):
	
	spotify = spotipy.Spotify(auth=token)
	user = spotify.current_user()['id']
	
	smaller_playlist = []
	larger_playlist = list(top_tracks)
	
	for key, values in top_tracks.items():
		if value == 0:
			smaller.playlist(key)
	
	user_playlists = spotify.current_user_playlists()
	
	user_playlists = user_playlists['items']
	
	small_playlist_id = None
	large_playlist_id = None
	for playlist in user_playlists:
		if playlist['name'] == small_playlist:
			small_playlist_id = playlist['uri']
		elif playlist['name'] == large_playlist:
			large_playlist_id = playlist['uri']
	
	if small_playlist_id == None:
		small_playlist_id = spotify.user_playlist_create(user=user, \
		name=small_playlist)['uri']
	if large_playlist_id == None