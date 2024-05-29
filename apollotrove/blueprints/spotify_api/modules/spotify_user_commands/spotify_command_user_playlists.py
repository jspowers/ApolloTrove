import logging
from apollotrove.blueprints.spotify_api.modules.spotify_assets.spotify_user_assets import SpotifyUserAssets
from apollotrove.utilities.mongoQL.mongo_spotify_user_playlist import MDBSpotifyUserPlaylistCollection


# ----------------------------- #
# User Playlist Data
# ----------------------------- #
class SpotifyCommandUserPlaylists(object): 
    user_assets = None
    user_playlists = None
    db_user_playlists = None

    def __init__(self, user_id, access_token):
        self.user_assets = SpotifyUserAssets()
        # TODO: logic for if playlists exists and hasn't been updated recently
        self.user_playlists = self.user_assets.get_spotify_user_playlists(access_token=access_token, user_id=user_id)
        self.db_user_playlists = MDBSpotifyUserPlaylistCollection(user_id = self.user_playlists['user_id'])

    # -------------------- #
    # - MongoDB METHODS - #
    def get_user_playlists(self): 
        return self.db_user_playlists.get_db_user_playlists() 

    def set_user_playlists(self,overwrite=False): 
        self.db_user_playlists.write_db_user_playlists(document=self.user_playlists,overwrite=overwrite)
        return

    def delete_user(self):
        self.db_user_playlists.remove_db_user_playlist()
        return