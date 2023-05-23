import logging
from spotify_assets.user_assets import UserAssets
from spotify_assets.playlist_assets import PlaylistAssets
from spotify_assets.track_assets import TrackAssets
from mongoQL.mongo_user import MDBUserCollection 
from mongoQL.mongo_user_playlist import MDBUserPlaylistCollection
from mongoQL.mongo_playlist import MDBPlaylistCollection

# ----------------------------- #
# User Profile Data
# ----------------------------- #
class CommandUser(object): 
    user_assets = None
    user_profile = None
    db_user = None

    def __init__(self, user_id, access_token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_assets = UserAssets()
        if user_id != None:
            self.user_profile = self.user_assets.get_user_public_profile(
                user_id=user_id
                ,access_token=access_token
                )
            self.db_user = MDBUserCollection(self.user_profile["id"])
        else:
            logging.warning("User ID not provided")
    
    def get_user(self): 
        return self.db_user.get_db_user_profile() 

    def set_user(self): 
        return self.db_user.write_db_user_profile(document=self.user_profile)

    def delete_user(self):
        return self.db_user.remove_db_user_profile()


# ----------------------------- #
# User Playlist Data
# ----------------------------- #
class CommandUserPlaylists(object): 
    user_assets = None
    user_playlists = None
    db_user = None

    def __init__(self, user_id, access_token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_assets = UserAssets()
        self.user_playlists = self.user_assets.get_user_playlists(access_token=access_token, user_id=user_id)
        self.db_user = MDBUserPlaylistCollection(user_id = self.user_playlists['user_id'])

    # -------------------- #
    # - MongoDB METHODS - #
    def get_user_playlists(self): 
        return self.db_user.get_db_user_playlists() 

    def set_user_playlists(self): 
        return self.db_user.write_db_user_playlists(document=self.user_playlists)

    def delete_user(self):
        return self.db_user.remove_db_user_playlist()





# ----------------------------- #
class CommandPlaylists(object):
    playlists_assets = None # spotify API commands
    user_asset = None # spotify API commands
    db_playlist = None # mongoDB playlists collection
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlists_assets = PlaylistAssets()
        self.db_user = MDBPlaylistCollection()

    def generate_playlist_list(self, access_token, playlists):
        playlist_data = []
        playlist_iterator = 0
        total_playlist_count = len(playlists)
        for playlist_id in playlists:
            playlist_data.append(self.playlists_assets.get_playlist(access_token, playlist_id))
            playlist_iterator += 1
            logging.info(f"Playlist {playlist_iterator}/{total_playlist_count} collected.")
        print(len(playlist_data))
        return playlist_data
        
    # -------------------- #
    # - MongoDB METHODS - #
    def get_user_playlists(self):
        return 

    def get_set_playlist(self):
        return

    def delete_playlist(self):
        return