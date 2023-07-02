import requests

class TrackAssets(object):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_spotify_track(self, access_token, track_id, market=''):
        token_header = {'Authorization': f'Bearer {access_token}'}
        url_ = f'https://api.spotify.com/v1/tracks/{track_id}'
        r = requests.get(url_, headers=token_header)
        return r.json()
    
    def get_spotify_tracks(self, access_token, track_ids=[]):
        tracks_string = ','.join(track_ids)
        token_header = {'Authorization': f'Bearer {access_token}'}
        url_ = f'https://api.spotify.com/v1/tracks?market=US&ids={tracks_string}'
        r = requests.get(url_, headers=token_header)
        return r.json()