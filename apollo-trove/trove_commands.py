from spotify_assets.user_assets import UserAssets
from spotify_assets.playlist_assets import PlaylistAssets
from spotify_assets.track_assets import TrackAssets
from mongoQL.mongo_user import MDBUserCollection 
from mongoQL.mongo_user_playlist import MDBUserPlaylistCollection

# ----------------------------- #
# User Profile Data
# ----------------------------- #
class CommandUser(object): 
    user = None
    user_profile = None
    db_user = None

    def __init__(self, user_id, access_token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = UserAssets()
        self.user_profile = self.user.get_user_public_profile(access_token=access_token, user_id=user_id)
        self.db_user = MDBUserCollection(self.user_profile['id'])

    def get_user(self): 
        return self.db_user.get_db_user_profile() 

    def set_user(self): 
        return self.db_user.write_db_user_profile(document=self.user_profile)

    def delete_user(self):
        return self.db_user.remove_db_user_profile()


# ----------------------------- #
# User Profile Data
# ----------------------------- #
class CommandUserPlaylists(object): 
    user = None
    user_playlists = None
    db_user = None

    def __init__(self, user_id, access_token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = UserAssets()
        self.user_playlists = self.user.get_user_playlists(access_token=access_token, user_id=user_id)
        self.db_user = MDBUserPlaylistCollection(self.user_playlists['user_id'])

    # def get_user(self): 
    #     return self.db_user.get_db_user_profile() 

    def set_user_playlists(self): 
        return self.db_user.write_db_user_playlists(document=self.user_playlists)

    # def delete_user(self):
    #     return self.db_user.remove_db_user_profile()
