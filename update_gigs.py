# import
import localgigs

api = '' # The Songkick API key
metro = '' # Metro ID for the area
gigs = localGig(apikey = api, metro = metro)

if __name__ == "__main__":
    # get the songkick xml and split artist
    # into 3 categories, one  in next 7 days
    # next 2 months,
    # every gig listed beyond that
    gigs.get_songkick(day_splits = [7, 60]
    
    # get the uniform resource identifier for
    # each artist listed, if they are on spotify
    gigs.get_artist_uri()
    
    # get the top n tracks uri for each artist
    gigs.get_tracks(n_tracks = 2)
    
    # make or update playlist
    gigs.update_playlist(playlist_names = ['', '', ''])