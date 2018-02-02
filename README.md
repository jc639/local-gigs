# Python script for updating your Spotify with local gigs

## Description

Uses Songkick's API to obtain all the local gigs in
a given metro area and then using Spotipy, a thin client
library for the Spotify Web API, it updates three playlists
on your user account. 

Spotipy's full documentation is [here](http://spotipy.readthedocs.org/)
and github is [here](https://github.com/plamere/spotipy)

## How to use

There are several things you need to do to get this to work and I
can make no guarantee that they are all possible...

1. Install [spotipy](https://github.com/plamere/spotipy) by following instructions in the link
2. Register as developer on Spotify, and register your app which you need to use the client
details to authorise. Details on how to do this are in the spotipy [documentation](http://spotipy.readthedocs.org/)
3. These client details need to be plugged into the localgigs.py file for OAuth2 authorisation, the details of which are in the spotipy docs.
3. Finally you would need to get a Songkick API which you can read about [here.](https://www.songkick.com/developer) 
There are some [terms](https://www.songkick.com/developer/api-terms-of-use) that need to be met to get one,
and you need to give specifics details of what you are doing. The API key is needed in new instance of localgigs object.

## Finally
I am running this on Raspberry Pi, thats always on, so I just scheduled it to run at 1:00am everyday
with the following commands:

```
crontab -e

0 1 * * * cd /home/pi/local-gigs && ./update_gigs.py
```

Obviously change directory to where script is located on your Pi.

And the output:
[All gigs in Cambridge](https://open.spotify.com/user/slothy123/playlist/3SwUqPw2AfjrnJgbPRel9e?si=uWMh1ZjWQyeVoFqjuAmC0Q)

[Cambridge gigs in next two months](https://open.spotify.com/user/slothy123/playlist/6VmM1CaAl8N1CASqtokcKS?si=5TUosc1RTPSvrKFd8833DQ)

[Cambridge gigs in next seven days](https://open.spotify.com/user/slothy123/playlist/3B8FpvIHyzHAxcPOmlGiMq?si=JcVCqTabRtSIaNkIQKgXIQ)