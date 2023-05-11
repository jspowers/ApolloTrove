import json 
import requests

class PlaylistAssets(object):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_playlist(self, access_token=None, playlist_id=None):
        token_header = {'Authorization': f'Bearer {access_token}'}
        url_ = f'https://api.spotify.com/v1/playlists/{playlist_id}'
        r = requests.get(url_, headers=token_header)
        return r.json()
    
    def get_playlist_tracks(self, access_token, playlist_id):
        track_list = []
        track_meta = []
        token_header = {'Authorization': f'Bearer {access_token}'}
        url_ = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        next_get = ''
        
        while (next_get != None):
            r = requests.get(url_, headers=token_header).json()
            for track in r['items']:
                track_list.append(track['track']['name'])
                track_meta.append(track)
            next_get = r['next']
            url_ = next_get
        return track_list, track_meta 
    
