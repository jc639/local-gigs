#!/usr/bin/python3

# import modules
import requests
import xml.etree.ElementTree as ET
import datetime as dt
import spotipy
import spotipy.util as util
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

        # empty data structures, modified by functions
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

					# dictionary with artist name as key, value
					# represents where there gig falls
					# 0 in the playlist for next few days
					# 1 for the longer one
					# 2 for anything outside 
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
		
        # gets the artist URI on Spotify if they exist
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
	
    def get_tracks(self, n_tracks = 2):
        '''
        Gets the top tracks for the artists.

        Parameters:
        1. n_tracks - Number of top tracks you want, default 
        is two. If number of tracks available is shorter than n_tracks it
        returns the total number of tracks for that artist.
        '''

        # iterate through the artist uri
        for key, value in self.artist_uris.items():
            results = sp.artist_top_tracks(value)

            # refine results down to tracks
            results = results['tracks']
            
            # if length of results is shorter than n_tracks
            # get all
            # update the track dictionary with track uri and associated
            # value of which playlist
            if len(results) < n_tracks:
                for tracks in results:
                    self.tracks.update({tracks['uri'] : self.artists[key]})
            else:
                for tracks in results[: n_tracks]:
                    self.tracks.update({tracks['uri'] : artist[key]})

    def update_playlists(self, playlist_names = None):
        '''
        Update/Create the playlists

        Parameters:
        1. playlist_names - List of names that you want the playlist
        to be called. Length of 3, in order of small, medium, large.
        '''

        # get your user id
        user = sp.current_user()['id']
        
        # three playlist
        # small - soon, large and everything
        sm_playlist = []
        lg_playlist = []
        all_playlist = list(self.tracks)

        # iterate through key, vals and
        # assign tracks to correct playlist
        # on basis of value
        for key, value in top_tracks.items():
            if value == 0:
                sm_playlist.append(key)
                lg_playlist.append(key)
            elif value == 1:
                lg_playlist.append(key)

        # get the users playlist that already exist
        user_playlists = sp.current_user_playlists()
        user_playlists = user_playlists['items']

        # set ids as none
        sm_id = None
        lg_id = None
        all_id = None

        # iterate through existing playlists
        # if exist get their uri
        for playlist in user_playlists:
            if playlist['name'] == playlist_names[0]:
                sm_id = playlist['uri']
            elif playlist['name'] == playlist_names[1]:
                lg_id = playlist['uri']
            elif playlist['name'] == playlist_names[2]:
                all_id = playlist['uri']

        # if ids are still none create the playlist
        if sm_id == None:
            sm_id = sp.user_playlist_create(user = user, name = playlist_names[0])['uri']
        if lg_id == None:
            lg_id = sp.user_playlist_create(user = user, name = playlist_names[1])['uri']
        if all_id == None:
           all_id = sp.user_playlist_create(user = user, name = playlist_names[2])['uri']

        # list ids and playlist
        ids = [sm_id, lg_id, all_id]
        playlists = [sm_playlist, lg_playlist, all_playlist]

        # iterate through, spotipy can 
        # only put <=100 songs into a playlist
        # if longer split
        for i in range(0, len(ids)):
            tracks = playlists[i]

            if len(tracks) <= 100:
                sp.user_playlist_replace_tracks(user = user, playlist_id = ids[i],
                tracks = tracks)

            # where its longer, split
            else:
                t = [tracks[j : j+100] for j in range(0, len(tracks), 100)]
                for k in range(0, len(t)):
                    # on initial replace
                    if k == 0:
                        sp.user_playlist_replace_tracks(user = user, playlist_id = ids[i],
                        tracks = t[k])
                    # on next just add track
                    else:
                        sp.user_playlist_add_tracks(user = user, playlist_id = ids[i],
                        tracks = t[k])