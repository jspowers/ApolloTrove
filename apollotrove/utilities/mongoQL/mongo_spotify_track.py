from .mongo_operators import (open_collection, mongo_get, mongo_set, mongo_delete)
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

"""
Class: MDBPSpotifyTrackCollection


"""
class MDBSpotifyTrackCollection(object):
    track_collection = None

    def __init__(self):
        self.track_collection = open_collection("core","tracks")

    def get_db_track(self,documents,document_key="id"):
        track_data = []
        for doc in documents:
            query_response = mongo_get(
                primary_key=document_key,
                ref_id=doc[document_key],
                collection=self.track_collection,
            )
            track_data.append(query_response)
        return track_data
        

    def write_db_track(self, documents, documeent_key="id",overwrite=False):
        for doc in documents:
            mongo_set(
                primary_key=documeent_key,
                ref_id=doc[documeent_key],
                insert_document=doc,
                collection=self.track_collection,
                overwrite=overwrite,
            )
        return
    
    def remove_db_track(self, doc_keys, document_key = "id"):
        for key in doc_keys:
            mongo_delete(
                primary_key=document_key,
                ref_id=key,
                collection=self.track_collection,
            )
        return