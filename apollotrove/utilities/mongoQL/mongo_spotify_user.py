from .mongo_operators import (open_collection, mongo_get, mongo_set, mongo_delete)
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

"""
PyMongo Tutorial
https://pymongo.readthedocs.io/en/stable/tutorial.html

Class: MDBSpotifyUserCollection
Methods:
    get_db_user_profile()
    write_db_user_profile()
    remove_db_user_profile() 
"""

class MDBSpotifyUserCollection(object):
    user_collection = None
    mongo_user_id = None
    
    def __init__(self, user_id):
        self.mongo_user_id = user_id
        self.user_collection = open_collection("core", "users")

    # ------------------------ #
    # USER PROFILE
    # Methods for interacting with user profiles
    # API Endpoints: https://developer.spotify.com/documentation/web-api/reference/get-users-profile
    # ------------------------ #
    def get_db_user_profile(self, document_key = "id"):
        user_profile = mongo_get(
            primary_key=document_key,
            ref_id=self.mongo_user_id,
            collection=self.user_collection,
        )
        return user_profile
    
    # ------------------------ #
    # Feed in spotify profile to insert/replace existing records
    # ------------------------ #
    def write_db_user_profile(self, document=None, document_key = "id", overwrite=False):
        mongo_set(
            primary_key=document_key,
            ref_id=self.mongo_user_id,
            collection = self.user_collection,
            insert_document=document,
            overwrite=overwrite,
            )
        return
    
    def remove_db_user_profile(self,document_key="id"):
        mongo_delete(
            primary_key=document_key,
            ref_id=self.mongo_user_id,
            collection=self.user_collection,
        )
        return
        
    