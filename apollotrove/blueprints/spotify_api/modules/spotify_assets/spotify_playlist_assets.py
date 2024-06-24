import requests

from apollotrove.utilities.py_utilities import encode_url_request
from datetime import datetime

class SpotifyPlaylistAssets():

    @staticmethod
    def get_spotify_playlist(access_token, playlist_id):
        playlist_field_filters = [
            'id',
            'name',
            'collaborative',
            'description',
            'followers.total',
            'public',
            'owner.id',
            'owner.display_name',
            'tracks(href,limit,next,offset,previous,total,items(added_by.id,track(id,name,href,artists.name)))',
        ]

        next_track_field_filters = [
            'href',
            'limit',
            'next',
            'offset',
            'previous',
            'total',
            'items(added_by.id,track(id,name,href,artists.name))',
        ]

        token_header = {'Authorization': f'Bearer {access_token}'}
        url_ = f'https://api.spotify.com/v1/playlists/{playlist_id}?market=US&fields=' + ','.join(playlist_field_filters)
        request_ts = datetime.now()
        r = requests.get(url_, headers=token_header)

        # Setting up logic for playlists longer than 100 items
        result = r.json()
        result['request_ts'] = request_ts

        next_get = result['tracks']['next']
        
        if result['tracks']['next'] == None:
            return result
        else:
            # Create Track Bank to store results
            track_bank = result['tracks']['items']
        
            # Build URL string for the GET Request
            # BOTH LIMIT AND OFFSET get same value on first NEXT
            offset = result['tracks']['limit']
            limit = result['tracks']['limit']
            field_filter = ','.join(next_track_field_filters)
            url_ = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={offset}&limit={limit}&market=US&fields={field_filter}' 


            while next_get != None:
                # API call changes for NEXT url, not original dict schema
                r = requests.get(url_, headers=token_header)
                temp_result = r.json()
            
                track_bank.extend(temp_result['items'])
                # next_get = encode_url_request(temp_result['next'])
                
                next_get = temp_result['next']
                url_ = next_get
            result['tracks']['items'] = track_bank
            
            return result
    
