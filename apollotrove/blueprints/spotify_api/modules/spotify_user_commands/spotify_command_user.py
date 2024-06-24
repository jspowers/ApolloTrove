import logging
from apollotrove.blueprints.spotify_api.modules.spotify_assets.spotify_user_assets import SpotifyUserAssets
from apollotrove.utilities.mongoQL.mongo_spotify_user import MDBSpotifyUserCollection 

# ----------------------------- #
# User Profile Data
# ----------------------------- #
class SpotifyCommandUser(object): 
    user_assets = None
    user_profile = None
    db_user = None

    def __init__(self, user_id, access_token):
        self.user_assets = SpotifyUserAssets()
        if user_id != None:
            self.user_profile = self.user_assets.get_spotify_user_public_profile(
                user_id=user_id
                ,public_access_token=access_token
                )
            self.db_user = MDBSpotifyUserCollection(self.user_profile["id"])
        else:
            logging.warning("User ID not provided")
    
    def get_user(self): 
        return self.db_user.get_db_user_profile() 

    def set_user(self,overwrite=False): 
        self.db_user.write_db_user_profile(document=self.user_profile,overwrite=overwrite)
        return

    def delete_user(self):
        self.db_user.remove_db_user_profile()
        return