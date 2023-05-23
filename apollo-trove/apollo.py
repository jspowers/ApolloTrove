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
at_instance_user = "jspowers"  # <- SET USER ID HERE
at_instance = ATUser(user_id=at_instance_user, access_token=access_token)


playlists = at_instance.user_playlist_command.user_playlists['items']
playlist_ids = [playlist["id"] for playlist in playlists]
"""
PICK UP HERE 

- STORE THE LIST OF USER PLAYLISTS TO MONGO DB
- NARROW THE GET_PLAYLIST FUNCTION TO ONLY BRING IN SOME FIELDS
- IMPLEMENT ASYNC TO PULL DATA MORE EFFECIENTLY

"""
pl_docs = at_instance.playlist_command.generate_playlist_list(access_token=access_token, playlists=playlist_ids)