import logging
from spotify_assets.user_assets import UserAssets
from spotify_assets.playlist_assets import PlaylistAssets
from spotify_assets.track_assets import TrackAssets
from mongoQL.mongo_user import MDBUserCollection 
from mongoQL.mongo_user_playlist import MDBUserPlaylistCollection
from mongoQL.mongo_playlist import MDBPlaylistCollection
from mongoQL.mongo_track import MDBTrackCollection

# ----------------------------- #
# User Profile Data
# ----------------------------- #
class CommandUser(object): 
    user_assets = None
    user_profile = None
    db_user = None

    def __init__(self, user_id, access_token):
        self.user_assets = UserAssets()
        if user_id != None:
            self.user_profile = self.user_assets.get_spotify_user_public_profile(
                user_id=user_id
                ,access_token=access_token
                )
            self.db_user = MDBUserCollection(self.user_profile["id"])
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


# ----------------------------- #
# User Playlist Data
# ----------------------------- #
class CommandUserPlaylists(object): 
    user_assets = None
    user_playlists = None
    db_user_playlists = None

    def __init__(self, user_id, access_token):
        self.user_assets = UserAssets()
        # TODO: logic for if playlists exists and hasn't been updated recently
        self.user_playlists = self.user_assets.get_spotify_user_playlists(access_token=access_token, user_id=user_id)
        self.db_user_playlists = MDBUserPlaylistCollection(user_id = self.user_playlists['user_id'])

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




# ----------------------------- #
# Playlist Details
# ----------------------------- #
class CommandPlaylists(object):
    playlists_assets = None # spotify API commands
    playlist_data = None
    db_playlist = None # mongoDB playlists collection
    
    def __init__(self, playlist_ids, access_token):
        self.playlists_assets = PlaylistAssets()
        self.get_spotify_playlist_list(playlist_ids=playlist_ids,access_token=access_token)
        self.db_playlist = MDBPlaylistCollection()

    # -------------------- #
    # - Spotify API METHODS - #
    def get_spotify_playlist_list(self, access_token, playlist_ids):
        # TODO: logic for if playlists exists and hasn't been updated recently
        playlist_data = []
        playlist_iterator = 0
        total_playlist_count = len(playlist_ids)
        for playlist_id in playlist_ids:
            playlist_data.append(self.playlists_assets.get_spotify_playlist(access_token, playlist_id))
            playlist_iterator += 1
            logging.info(f"Playlist {playlist_iterator}/{total_playlist_count} collected.")
            # ----------------- #
            # TESTING CONDITION
            if playlist_iterator == 10:
                break
            # ----------------- #
        logging.info(f"Retrieved {len(playlist_data)} playlists")
        self.playlist_data = playlist_data
        return
        
    # -------------------- #
    # - MongoDB METHODS - #
    def get_user_playlists(self,documents):
        return self.db_playlist.get_db_playlist(documents=documents)

    def set_playlist(self,overwrite):
        self.db_playlist.write_db_playlist(self.playlist_data,overwrite=overwrite)
        return

    def delete_playlist(self,keys):
        self.db_playlist.remove_db_playlist(doc_keys=keys)
        return
    

# ----------------------------- #
# Track Details
# ----------------------------- #
class CommandTracks(object):
    track_assets = None
    db_track = None

    def __init__(self):
        self.track_assets = TrackAssets()
        self.db_track = MDBTrackCollection()

    # -------------------- #
    # - Spotify API METHODS - #
    def get_spotify_track_assets(self, track_ids, access_token):
        #check if track already exists in mongo DB
        # skippable_tracks = [track_id for track_id in track_ids if self.get_tracks(track_id) != None]
        skippable_tracks = []
        track_tasks = [task for task in track_ids if task not in skippable_tracks]
        # spotify API rate limit for batch requests = 50 Tracks
        # https://developer.spotify.com/documentation/web-api/reference/get-several-tracks
        batch_size = 50
        track_batch = [track_tasks[track * batch_size:(track + 1) * batch_size] for track in range((len(track_tasks)+batch_size-1)//batch_size)]
        batch_iterator = 0
        track_data = []
        logging.info(f"Track Batch Runs: {len(track_batch)} required.")
        for batch in track_batch:
            r = self.track_assets.get_spotify_tracks(access_token=access_token,track_ids=batch)
            track_data.append(r['tracks'])
            batch_iterator += 1
            logging.info(f"Track batch {batch_iterator}/{len(track_batch)} collected.")        
        return track_data

    # -------------------- #
    # - TRANSFORMATION METHODS - #
    def prepare_playlist_trackids(playlist_data):
        tracks = []
        for playlist in playlist_data:
            pl_len = len(playlist['tracks']['items'])
            pl_name = playlist['name']
            logging.info(f"Gathering IDs for {pl_len} tracks in '{pl_name}'")
            for track in playlist['tracks']['items']:
                tracks.append(track['track']['id'])     
        track_set = set(tracks)
        tracks = list(track_set)
        return tracks

    # -------------------- #
    # - MongoDB METHODS - #
    # TODO: Write mongo track methods
    def get_tracks(self, documents):
        return self.db_track.get_db_track(documents=documents)
    
    def set_tracks(self, documents):
        self.db_track.write_db_track(documents=documents)
        return
    
    def delete_tracks(self,keys):
        self.db_track.remove_db_track(doc_keys=keys)
        return