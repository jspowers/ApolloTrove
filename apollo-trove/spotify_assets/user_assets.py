import requests
import logging

class UserAssets(object):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_spotify_user_public_profile(self, access_token, user_id):
        if user_id == None or user_id == "":
            logging.warning("No userID given, ending get request")
            return
        token_header = {'Authorization': f'Bearer {access_token}'}
        url_ = f"https://api.spotify.com/v1/users/{user_id}"
        r = requests.get(url_, headers=token_header)
        logging.info(f"API response status code: {r.status_code}")
        return r.json()

    def get_spotify_user_playlists(self, access_token = None, user_id = None):
        user_playlist_meta = []
        # user_playlist_list = []
        # user_playlist_ids = []
        token_header = {'Authorization': f'Bearer {access_token}'}
        url_ = f'https://api.spotify.com/v1/users/{user_id}/playlists'
        next_get = ''
        while (next_get != None):
            r = requests.get(url_, headers=token_header).json()
            for playlist in r['items']:
                # user_playlist_list.append(playlist['name'])
                # user_playlist_ids.append(playlist['id'])
                user_playlist_meta.append(playlist)
            next_get = r['next']
            url_ = next_get
        
        return {
            "user_id": user_id,
            "items": user_playlist_meta
            }
        # TEMP - ONLY RETURN TOTAL META
        # return {
        #     "playlist_meta": user_playlist_meta,
        #     "playlist_names": user_playlist_list,
        #     "playlist_ids": user_playlist_ids
        # }