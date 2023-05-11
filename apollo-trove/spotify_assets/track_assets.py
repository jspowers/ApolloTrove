import json 
import requests

class TrackAssets(object):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_track(self, access_token=None, track_id=None):
        token_header = {'Authorization': f'Bearer {access_token}'}
        url_ = f'https://api.spotify.com/v1/tracks/{track_id}'
        r = requests.get(url_, headers=token_header)
        return r.json()