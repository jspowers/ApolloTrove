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

    def set_user(self,overwrite=False): 
        return self.db_user.write_db_user_profile(document=self.user_profile,overwrite=overwrite)

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
        # TODO: logic for if playlists exists and hasn't been updated recently
        self.user_playlists = self.user_assets.get_user_playlists(access_token=access_token, user_id=user_id)
        self.db_user = MDBUserPlaylistCollection(user_id = self.user_playlists['user_id'])

    # -------------------- #
    # - MongoDB METHODS - #
    def get_user_playlists(self): 
        return self.db_user.get_db_user_playlists() 

    def set_user_playlists(self,overwrite=False): 
        return self.db_user.write_db_user_playlists(document=self.user_playlists,overwrite=overwrite)

    def delete_user(self):
        return self.db_user.remove_db_user_playlist()




# ----------------------------- #
# Playlist Details
# ----------------------------- #
class CommandPlaylists(object):
    playlists_assets = None # spotify API commands
    db_playlist = None # mongoDB playlists collection
    playlist_data = None
    
    def __init__(self, playlist_ids, access_token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlists_assets = PlaylistAssets()
        self.generate_playlist_list(playlist_ids=playlist_ids,access_token=access_token)
        self.db_playlist = MDBPlaylistCollection()

    # -------------------- #
    # - Spotify API METHODS - #
    def generate_playlist_list(self, access_token, playlist_ids):
        # TODO: logic for if playlists exists and hasn't been updated recently
        playlist_data = []
        playlist_iterator = 0
        total_playlist_count = len(playlist_ids)
        for playlist_id in playlist_ids:
            playlist_data.append(self.playlists_assets.get_playlist(access_token, playlist_id))
            playlist_iterator += 1
            logging.info(f"Playlist {playlist_iterator}/{total_playlist_count} collected.")
        logging.info(f"Retrieved {len(playlist_data)} playlists")
        self.playlist_data = playlist_data
        return
        
    # -------------------- #
    # - MongoDB METHODS - #
    def get_user_playlists(self,documents):
        return self.db_playlist.get_db_playlist(documents=documents)

    def set_playlist(self,overwrite):
        return self.db_playlist.write_db_playlist(self.playlist_data,overwrite=overwrite)

    def delete_playlist(self,documents):
        return self.db_playlist.remove_db_playlist(documents=documents)
    

# ----------------------------- #
# Playlist Details
# ----------------------------- #
class CommandTracks(object):
    track_asset = None
    track_data = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # -------------------- #
    # - Spotify API METHODS - #
    def get_track_assets(self, track_ids, access_token):
        #check if track already exists in mongo DB
        skippable_tracks = [track_id for track_id in track_ids if self.get_tracks(track_id) != None]
        track_tasks = [task for task in track_ids if task not in skippable_tracks]

        # TODO: use track_tasks against spotify API with logic for accomodating max 50 songs in request
        # if len() <= 50 do task else yield rest into next job
        
        return

    # -------------------- #
    # - MongoDB METHODS - #
    # TODO: Write mongo track methods
    def get_tracks(self, documents):
        # function that pulls track data from mongoDB
        return
    
    def set_tracks(self, documents):
        # function that writes track data from mongoDB
        return
    
    def delete(self, documents):
        # function that deletes track data from mongoDB
        return