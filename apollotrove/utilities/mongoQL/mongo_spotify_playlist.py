from .mongo_operators import (open_collection, mongo_get, mongo_set, mongo_delete)
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

"""
Class: MDBSpotifyPlaylistCollection
"""

class MDBSpotifyPlaylistCollection(object):
    playlist_collection = None

    def __init__(self):
        self.playlist_collection = open_collection("core", "playlists")
    
    # # ------------------------ #
    # # USER PLAYLIST
    # # Methods for interacting with user Playlists
    # # API Endpoints: https://developer.spotify.com/documentation/web-api/reference/get-playlist
    # # ------------------------ #

    def get_db_playlist(self,documents,document_key="id"):
        playlist_data = []
        for doc in documents:
            query_response = mongo_get(
                primary_key=document_key,
                ref_id=doc[document_key],
                collection=self.playlist_collection,
            )
            playlist_data.append(query_response)
        return playlist_data
    
    def write_db_playlist(self,documents,document_key="id",overwrite=False):
        for doc in documents:
            mongo_set(
                primary_key=document_key,
                ref_id=doc[document_key],
                insert_document=doc,
                collection=self.playlist_collection,
                overwrite=overwrite
            )
        return

    def remove_db_playlist(self,doc_keys,document_key="id"): 
        for key in doc_keys:
            mongo_delete(
                primary_key=document_key,
                ref_id=key,
                collection=self.playlist_collection,
            )
        return