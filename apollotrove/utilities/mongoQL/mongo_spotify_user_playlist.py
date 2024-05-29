from .mongo_operators import (open_collection, mongo_get, mongo_set, mongo_delete)
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

"""
PyMongo Introduction
https://pymongo.readthedocs.io/en/stable/tutorial.html

Class: MDBSpotifyUserPlaylistCollection
"""

class MDBSpotifyUserPlaylistCollection(object):
    user_playlist_collection = None
    mongo_user_id = None

    def __init__(self, user_id):
        self.mongo_user_id = user_id
        self.user_playlist_collection = open_collection("core", "user_playlists")
    
    # # ------------------------ #
    # # USER PLAYLIST
    # # Methods for interacting with user Playlists
    # # API Endpoints: https://developer.spotify.com/documentation/web-api/reference/get-list-users-playlists
    # # ------------------------ #
    def get_db_user_playlists(self, document_key = "user_id"):
        user_playlists = mongo_get(
            primary_key=document_key,
            ref_id=self.mongo_user_id,
            collection=self.user_playlist_collection,
        )
        return user_playlists
    
    # ------------------------ #
    # Feed in spotify profile to insert/replace existing records
    # ------------------------ #
    def write_db_user_playlists(self,document=None,overwrite=False,document_key="user_id"):
        mongo_set(
            ref_id=self.mongo_user_id,
            collection = self.user_playlist_collection,
            insert_document=document,
            primary_key=document_key,
            overwrite=overwrite
            )
        return
    
    def remove_db_user_playlist (self, document_key = "user_id"):
        mongo_delete(
            primary_key=document_key,
            ref_id=self.mongo_user_id,
            collection=self.user_playlist_collection,
        )
        return
        