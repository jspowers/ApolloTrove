
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
    def get_db_user_profile(self):
        spotify_user = self.user_collection.find_one({"id":self.mongo_user_id})
        if spotify_user == None:
            logging.warning(f"User '{self.mongo_user_id}' not found in User Collection.")
            return
        return spotify_user
    
    # ------------------------ #
    # Feed in spotify profile to insert/replace existing records
    # ------------------------ #
    def write_db_user_profile(self, document=None):
        document_key="id"
        desired_overwrite=False
        mongo_set(
            ref_id=self.mongo_user_id,
            collection = self.user_collection,
            insert_document=document,
            primary_key=document_key,
            overwrite=desired_overwrite
            )
        return
    
    def remove_db_user_profile(self):
        if self.mongo_user_id == None:
            logging.warning("No profie provided - Skipping Delete")
            return
        mongo_record = self.user_collection.find_one({"id":self.mongo_user_id})
        spotify_user = mongo_record['id'] if mongo_record != None else None
        #Delete all instances where Spotify User exists
        count = self.user_collection.delete_many({"id":spotify_user}).deleted_count
        if count <= 0 or count == None:
            logging.warning("No users deleted from User collection.")
        else:
            logging.info(f"Spotify User {spotify_user} account information removed from User Collection.")
        return
        