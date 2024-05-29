import requests

class SpotifyPlaylistAssets():

    @staticmethod
    def get_spotify_playlist(access_token, playlist_id):
        token_header = {'Authorization': f'Bearer {access_token}'}
        url_ = f'https://api.spotify.com/v1/playlists/{playlist_id}?market=US'
        r = requests.get(url_, headers=token_header).json()
        
        # Setting up logic for playlists longer than 100 items
        result = r
        next_get = result['tracks']['next']
        if next_get == None:
            return result
        else:
            track_bank = result['tracks']['items']
            url_ = result['tracks']['next']
            while next_get != None:
                # API call changes for NEXT url, not original dict schema
                r = requests.get(url_,headers=token_header).json()
                for item in r['items']:
                    track_bank.append(item)
                next_get = r['next']
                url_ = next_get
            result['tracks']['items'] = track_bank
            return result
    