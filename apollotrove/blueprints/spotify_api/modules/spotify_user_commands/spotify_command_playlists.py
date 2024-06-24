import logging
from apollotrove.blueprints.spotify_api.modules.spotify_assets.spotify_playlist_assets import SpotifyPlaylistAssets
from apollotrove.utilities.mongoQL.mongo_spotify_playlist import MDBSpotifyPlaylistCollection

# ----------------------------- #
# Playlist Details
# ----------------------------- #
class SpotifyCommandPlaylists(object):
    playlists_assets = None # spotify API commands
    playlist_data = None
    db_playlist = None # mongoDB playlists collection
    
    def __init__(self, playlist_ids, access_token):
        self.playlists_assets = SpotifyPlaylistAssets()
        self.get_spotify_playlist_list(playlist_ids=playlist_ids,access_token=access_token)
        self.db_playlist = MDBSpotifyPlaylistCollection()

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
            # if playlist_iterator == 10:
                # break
            # ----------------- #
        logging.info(f"Retrieved {len(playlist_data)} playlists")
        self.playlist_data = playlist_data
        return
        
    # -------------------- #
    # - MongoDB METHODS - #
    def get_playlists(self,documents):
        return self.db_playlist.get_db_playlist(documents=documents)

    def set_playlist(self,overwrite):
        self.db_playlist.write_db_playlist(self.playlist_data,overwrite=overwrite)
        return

    def delete_playlist(self,keys):
        self.db_playlist.remove_db_playlist(doc_keys=keys)
        return