
from .pymongo_get_database import open_apollo_db
from .mongo_operators import (mongo_get, mongo_set, mongo_delete)
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

"""
PyMongo Introduction
https://pymongo.readthedocs.io/en/stable/tutorial.html

Class: MDBUserPlaylistCollection
"""

class MDBUserPlaylistCollection(object):
    user_playlist_collection = None
    mongo_user_id = None

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_user_id = user_id
        self.user_playlist_collection = self.open_collection("core", "user_playlists")
    
    #Return the database collection 
    def open_collection(self, db_name, collection_name):
        db_client = open_apollo_db()
        db = db_client[db_name]
        collection = db[collection_name]
        logging.info(f"successfully opened {db_name}.{collection_name}")
        return collection
    
    def close_user_collection(db_name=None):
        if db_name == None: 
            return
        db_name.close()
        return
    
    # # ------------------------ #
    # # USER PLAYLIST
    # # Methods for interacting with user Playlists
    # # API Endpoints: https://developer.spotify.com/documentation/web-api/reference/get-list-users-playlists
    # # ------------------------ #
    def get_db_user_playlists(self):
        document_key = "user_id"
        user_playlists = mongo_get(
            primary_key=document_key,
            ref_id=self.mongo_user_id,
            collection=self.user_playlist_collection,
        )
        return user_playlists
    
    # ------------------------ #
    # Feed in spotify profile to insert/replace existing records
    # ------------------------ #
    def write_db_user_playlists(self,document=None):
        document_key="user_id"
        desired_overwrite=False
        mongo_set(
            ref_id=self.mongo_user_id,
            collection = self.user_playlist_collection,
            insert_document=document,
            primary_key=document_key,
            overwrite=desired_overwrite
            )
        return
    
    def remove_db_user_playlist (self):
        document_key = "user_id"
        mongo_delete(
            primary_key=document_key,
            ref_id=self.mongo_user_id,
            collection=self.user_playlist_collection,
        )
        return
        