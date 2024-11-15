from datetime import datetime
from .spotify_utilities import get_batch_spotify_track_audio_features
import requests
import logging

class SpotifyTrackAssets():

    @staticmethod
    def get_spotify_track(access_token, track_id, market='US'):

        track_field_filters =[
            'id',
            'name',
            'popularity',
            'track_number',
            'duration_ms',
            'album.album_type',
            'album.id',
            'album.name',
            'album.type',
            'artists.name',
        ]

        token_header = {'Authorization': f'Bearer {access_token}'}
        request_ts = datetime.now()
        url_ = f'https://api.spotify.com/v1/tracks/{track_id}?market={market}&fields='+','.join(track_field_filters)
        r = requests.get(url_, headers=token_header)
        result = r.json()
        result['request_ts'] = request_ts
        logging.info(f"API response status code: {r.status_code}")
        return result
    
    @staticmethod
    def get_spotify_tracks(access_token, track_ids=[], market='US'):
        
        tracks_field_filters =['tracks(id,name,popularity,track_number,duration_ms,album.album_type,album.id,album.name,album.type,artists.name,artists.id)',]
        
        tracks_string = ','.join(track_ids)
        token_header = {'Authorization': f'Bearer {access_token}'}
        request_ts = datetime.now()
        url_ = f'https://api.spotify.com/v1/tracks?market={market}&ids={tracks_string}&fields='+','.join(tracks_field_filters)
        r = requests.get(url_, headers=token_header)
        result = r.json()
        result['request_ts'] = request_ts
        logging.info(f"API response status code: {r.status_code}")
        return result
