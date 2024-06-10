from datetime import datetime
import requests
import logging

class SpotifyUserAssets():
    
    @staticmethod
    def get_spotify_user_public_profile(public_access_token, user_id):
        if user_id == None or user_id == "":
            logging.warning("No userID given, ending get request")
            return
        token_header = {'Authorization': f'Bearer {public_access_token}'}
        url_ = f"https://api.spotify.com/v1/users/{user_id}"
        request_ts = datetime.now()
        r = requests.get(url_, headers=token_header)
        result = r.json()
        result['request_ts'] = request_ts
        logging.info(f"API response status code: {r.status_code}")
        return result

    @staticmethod
    def get_spotify_current_user_private_profile(access_token):
        token_header = {'Authorization': f'Bearer {access_token}'}
        url_ = "https://api.spotify.com/v1/me"
        request_ts = datetime.now()
        r = requests.get(url_, headers=token_header)
        result = r.json()
        result['request_ts'] = request_ts
        logging.info(f"API response status code: {r.status_code}")
        return result

    @staticmethod
    def get_spotify_user_playlists(access_token = None, user_id = None):
        user_playlist_meta = []
        # user_playlist_list = []
        # user_playlist_ids = []
        request_ts = datetime.now()
        token_header = {'Authorization': f'Bearer {access_token}'}
        url_ = f'https://api.spotify.com/v1/users/{user_id}/playlists'
        next_get = ''
        logging.info(f'Pulling User spotify playlists for {user_id} using {access_token}')
        while (next_get != None):
            r = requests.get(url_, headers=token_header).json()
            for playlist in r['items']:
                # user_playlist_list.append(playlist['name'])
                # user_playlist_ids.append(playlist['id'])
                user_playlist_meta.append(playlist)
            next_get = r['next']
            url_ = next_get        
        return {
            "request_ts": request_ts,
            "user_id": user_id,
            "items": user_playlist_meta
            }

    