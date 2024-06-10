from datetime import datetime
import requests
import logging

class SpotifyTrackAssets():
    
    @staticmethod
    def get_spotify_track(access_token, track_id, market='US'):
        token_header = {'Authorization': f'Bearer {access_token}'}
        request_time = datetime.now()
        url_ = f'https://api.spotify.com/v1/tracks/{track_id}?market={market}'
        r = requests.get(url_, headers=token_header)
        logging.info(f"API response status code: {r.status_code}")
        return {
            "request_ts": request_time,
            "result": r.json()
            }
    
    @staticmethod
    def get_spotify_tracks(access_token, track_ids=[], market='US'):
        tracks_string = ','.join(track_ids)
        token_header = {'Authorization': f'Bearer {access_token}'}
        request_time = datetime.now()
        url_ = f'https://api.spotify.com/v1/tracks?market={market}&ids={tracks_string}'
        r = requests.get(url_, headers=token_header)
        logging.info(f"API response status code: {r.status_code}")
        return {
            "request_ts": request_time,
            "result": r.json()
            }

#     @staticmethod
#     def get_spotify_track_features():
#         tracks_string = ','.join(track_ids)
#         token_header = {'Authorization': f'Bearer {access_token}'}
#         url_ = f'https://api.spotify.com/v1/tracks?market=US&ids={tracks_string}'
#         r = requests.get(url_, headers=token_header)
#         logging.info(f"API response status code: {r.status_code}")
#         return r.json()

#     def get_spotify_tracks_features():
        


# https://api.spotify.com/v1/audio-features/{id}



# https://api.spotify.com/v1/audio-features?ids=7ouMYWpwJ422jRcDASZB7P%2C4VqPOruhp5EdPBeR92t6lQ%2C2takcwOaAZWiXQijPHIx7B'


