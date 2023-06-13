
from .pymongo_get_database import open_apollo_db
from .mongo_operators import (mongo_get, mongo_set, mongo_delete)
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

"""
PyMongo Tutorial
https://pymongo.readthedocs.io/en/stable/tutorial.html

Class: MDBUserCollection
Methods:
    get_db_user_profile()
    write_db_user_profile()
    remove_db_user_profile() 
"""

class MDBUserCollection(object):
    user_collection = None
    mongo_user_id = None

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
    
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_user_id = user_id
        self.user_collection = self.open_collection("core", "users")

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
        
    