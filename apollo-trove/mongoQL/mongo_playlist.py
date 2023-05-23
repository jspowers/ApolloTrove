from .pymongo_get_database import open_apollo_db
from .mongo_operators import (mongo_get, mongo_set, mongo_delete)
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

"""
Class: MDBPlaylistCollection
"""

class MDBPlaylistCollection(object):
    playlist_collection = None
    mongo_playlist_id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playlist_collection = self.open_collection("core", "playlists")
    
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
    # # API Endpoints: https://developer.spotify.com/documentation/web-api/reference/get-playlist
    # # ------------------------ #

    def get_db_playlist(self):
        document_key = "playlist_id"
        playlist_data = mongo_get(
            primary_key=document_key,
            ref_id=self.mongo_playlist_id,
            collection=self.playlist_collection,
        )
        return playlist_data
    
    def set_db_playlist(self,documents):
        document_key="playlist_id"
        for doc in documents:
            mongo_set(
                primary_key=document_key,
                ref_id=self.mongo_playlist_id,
                insert_document=doc,
                collection=self.playlist_collection,
                overwrite=True
            )
    
    def remove_db_playlist(self): 
        document_key="playlist_id"
        mongo_delete(
            primary_key=document_key,
            ref_id=self.mongo_playlist_id,
            collection=self.playlist_collection,
        )