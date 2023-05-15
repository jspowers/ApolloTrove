import os 
import logging
from spotify_assets.spotify_api_auth import SpotifyAPIAuth
from trove_commands import (CommandUser,CommandUserPlaylists)


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
at_instance_user = "jspowers"  # <- SET USER ID HERE

# ----------------------------- #
# User Profile Data
# Methods: get_user(), set_user(), delete_user()
# ----------------------------- #
user_command = CommandUser(user_id=at_instance_user,access_token=access_token)
user_playlist_command = CommandUserPlaylists(user_id=at_instance_user,access_token=access_token)

#WIP playlist_command = CommandPlaylist( ,access_token=access_token)
#WIP track_command = CommandTrack( ,access_token=access_token)
