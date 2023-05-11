from pymongo import ReturnDocument
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

"""
PyMongo Introduction
https://pymongo.readthedocs.io/en/stable/tutorial.html

Creating reusable functions that can read/write to MongoDB
"""

def mongo_get():
    #START HERE
    return

def mongo_set(ref_id=None,collection=None,primary_key=None,insert_document=None,overwrite=False):
    if insert_document == None:
        logging.warning("No insert document provided - Skipping Write")
        return
    mongo_record = collection.find_one({primary_key:ref_id})
    mongo_id = mongo_record[primary_key] if mongo_record != None else None
    if mongo_id == None: 
        logging.info(f"Mongo ID ({mongo_id}) not found in collection. record will be created.")
    # Update (or insert) profile when overwrite is set to true
    # 1) Mongo record found and overwrite set to true OR if profile wasn't found
    if overwrite==True or mongo_id==None:
        inserted_id = collection.find_one_and_replace(
            filter={primary_key:ref_id},
            replacement=insert_document,
            upsert=True, # Insert if document doesn't exists
            return_document=ReturnDocument.AFTER,
            )[primary_key] 
        if inserted_id == None:
            logging.error("failed to update/write User document")
            return
        else:
            logging.info(f"wrote document to Mongo Collection with primary key: {inserted_id}")
            return
    # Log warning that user already exists and overwrite set to false
    elif overwrite==False and mongo_id!=None:
        logging.warning(f"no update/insert made. record for '{mongo_id}' already exists.")
        return
    logging.info("Updating actions completed")
    return


def mongo_delete():
    #START HERE
    return