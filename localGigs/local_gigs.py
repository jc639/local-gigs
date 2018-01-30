import requests
import xml.etree.ElementTree as ET
import os
import datetime as dt
import spotipy
import spotipy.util as util
import sys
import time
from math import ceil


# create Spotify API object
scope = 'playlist-modify-public'
user = 'your-user-name' # replace with your Spotify username
client_id='your-app-redirect-url' # replace with your client id from Spotify Dev
client_secret='your-app-redirect-url' # replace with your client id from Spotify Dev
redirect_uri='your-app-redirect-url' # replace with your client id from Spotify Dev

# first time you import this will being up authorisation window
# after that token will be cached and refresh
token = util.prompt_for_user_token(user, scope, client_id, client_secret,
redirect_uri)

# Authorised spotify API, with scope to modify playlist
sp = spotipy.Spotify(token)

# definition of gigs object and associated methods
class localGigs:
	'Updates your spotify with local gigs derived from songkick'

	def __init__(self, apikey, metro):
		'''
			Creates localGigs object
			
			Init parameter:
			1. apikey - API Key from Songkick
			2. metro  - Metro ID associated with area
		'''
		self.apikey = apikey
		self.metro = metro
		
		# empty dictonary, modified by functions
		self.artists = {}
		self.artist_uris = {}
		self.tracks = {}


	def get_songkick(self, day_splits=[]):
		'''
			Opens connection to Songkick XML
			and returns artists within given periods
			
			Params:
			1. day_splits = should be passed as a list with length
			of 2. First number is how many days from todays date that
			you would like the shorter, immediate playlist to cover. Second
			one is intermediate playlist. A third playlist is generated
			that covers absolutely everything listed
		'''
		# open connection to songkick API to get first page of XML
		address = 'http://api.songkick.com/api/3.0/metro_areas/' + self.metro + '/calendar.xml?apikey=' + self.apikey 
		r = requests(address)
		
		# root the XML tree
		root = ET.fromstring(r.text)
		r.close()
		
		# determine max number of pages
		total_entries = int(root.get('totalEntries'))
		n_pages = ceil(total_entries / 50)
		
		date_today = dt.datetime.now()
		short_cutdate = date_today + dt.timedelta(days = day_splits[0])
		long_cutdate = date_today + dt.timedelta(days = day_splits[1])
		
		# iterate through events and record which point they occur
		# covers first page, then iterates through the others
		for i in range(1, n_pages + 1)
			
			if i == 1:
				continue
			else:
				payload = {'page' : str(i)}
				r = requests.get(address, params = payload)
				root = ET.fromstring(r.text)
				r.close()
				
			for event in root.iter('event'):
				for start in event.iter('start'):
					start = dt.datetime.strptime(start.get('date'), '%Y-%m-%d')
				for artist in event.iter('artist'):
					artist = artist.get('displayName')
				
									
					if start < date_today + short_cutdate:
						self.artists.update({artist:0})

					elif start > short_cutdate and start < long_cutdate:
						self.artists.update({artist:1})
				
					else:
						self.artists.update({artist:2})

	def get_artist_uri(self):
		'''
		Gets the artist URI through the Spotify API
		'''
		artists = list(self.artists)
		
		for artist in artists:
			results = sp.search(q='artist:'+artist, type='artist', limit=1)
			
			if len(results['artists']['items']) != 0:
				results = results['artists']['items'][0]
				if results['name'].lower() == artist.lower():
					self.artist_uris.update({artist:results['uri']})
				elif results['name'].lower().replace(' & ', ' and ') == artist.lower():
					self.artist_uris.update({artist:results['uri']})
				elif results['name'].lower().replace(' and ', ' & ') == artist.lower():
					self.artist_uris.update({artist:results['uri']})
