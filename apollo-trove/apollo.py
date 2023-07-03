import os 
import logging
from spotify_assets.spotify_api_auth import SpotifyAPIAuth
from at_user.at_user_instance import ATUser


logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

CLIENT_ID = os.getenv('client_id', 'client_id Path Not Found')
CLIENT_SECRET = os.getenv('client_secret', 'client_secret Path Not Found')

auth_client = SpotifyAPIAuth(CLIENT_ID, CLIENT_SECRET)
auth_client.perform_auth()
access_token = auth_client.access_token
access_token_expires = auth_client.access_token_expires
logging.info(f"Access Token: {access_token} - Expires: {access_token_expires}")


# --------------------------------------- #
# --  START HERE WITH SPOTIFY USER ID  -- #

# Establish user instance
at_instance_user = "1260713492"  # <- SET USER ID HERE
at_instance = ATUser(user_id=at_instance_user, access_token=access_token)


# Open user instance commands
at_instance.open_user_commands()
at_instance.open_user_playlist_commands()
at_instance.open_playlist_commands()
at_instance.open_track_commands()


pl_data = at_instance.playlist_command.playlist_data
tracks = []

for playlist in pl_data:
    pl_len = len(playlist['tracks']['items'])
    pl_name = playlist['name']

    logging.info(f"Gathering IDs for {pl_len} tracks in '{pl_name}'")
    for track in playlist['tracks']['items']:
        tracks.append(track['track']['id'])


print(len(tracks))
track_set = set(tracks)
print(len(track_set))
tracks = list(track_set)




##### NOTES #####
# Playlist data is stored in
# at_instance.playlist_command.playlist_data[0]['tracks']['items']
# then 
# >>> test_ids = []
# >>> for track in playlist_test: 
# ...     test_ids.append(track['track']['id'])

"""
playlist_data
    [o] LOOP
        ['tracks']['items']
            [o] LOOP
                ['track']['id']
"""



"""
# TODO List:
- [ ] NARROW THE GET_PLAYLIST FUNCTION TO ONLY BRING IN SOME FIELDS
- [ ] Managing orphaned playlists in MongoDB
"""
