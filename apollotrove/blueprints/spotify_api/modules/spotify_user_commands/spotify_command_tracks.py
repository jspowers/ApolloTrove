import logging
from apollotrove.blueprints.spotify_api.modules.spotify_assets.spotify_track_assets import SpotifyTrackAssets
from apollotrove.utilities.mongoQL.mongo_spotify_track import MDBSpotifyTrackCollection
from apollotrove.utilities.py_utilities import array_flatten


# ----------------------------- #
# Track Details
# ----------------------------- #
class SpotifyCommandTracks(object):
    track_assets = None
    db_track = None
    track_data = None

    def __init__(self):
        self.track_assets = SpotifyTrackAssets()
        self.db_track = MDBSpotifyTrackCollection()

    # -------------------- #
    # - Spotify API METHODS - #
    def get_spotify_track_assets(self, track_ids, access_token):
        """
        Use the spotify API to get track details for a list of track_ids.
        Results are returned in a list[list[dictionaries]] (not a typo - don't kill me). 
        Each index of the list contains a batch of 50 tracks.
        """
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
        # Flatten the batched results
        flat_track_data = list(array_flatten(track_data))
        self.track_data = flat_track_data
        return 

    # -------------------- #
    # - TRANSFORMATION METHODS - #
    @staticmethod
    def prepare_playlist_trackids(playlist_data):
        tracks = set()
        # TimeComp: O(n * m)
        for playlist in playlist_data:
            pl_len = len(playlist['tracks']['items'])
            pl_name = playlist['name']
            logging.info(f"Gathering IDs for {pl_len} tracks in '{pl_name}'")
            for track in playlist['tracks']['items']:
                if track['track']['id'] != None:
                    tracks.add(track['track']['id'])
                else:
                    logging.warning(f"Skipping song {track['track']['name']}: No ID found.")
        return tracks

    # -------------------- #
    # - MongoDB METHODS - #
    def get_tracks(self, documents):
        return self.db_track.get_db_track(documents=documents)
    
    def set_tracks(self, documents, overwrite=False):
        # self.db_track.write_db_track(documents=documents, overwrite=overwrite)
        self.db_track.write_db_track(documents=documents, overwrite=True)
        return
    
    def delete_tracks(self,keys):
        self.db_track.remove_db_track(doc_keys=keys)
        return