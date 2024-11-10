from pymongo import ReturnDocument, InsertOne, ReplaceOne
from .pymongo_get_database import open_apollo_db
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

"""
PyMongo Introduction
https://pymongo.readthedocs.io/en/stable/tutorial.html

Creating reusable functions that can read/write to MongoDB
"""

def open_collection(db_name, collection_name):
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

def mongo_get(primary_key, ref_id, collection):
    mongo_record = collection.find_one({primary_key:ref_id})
    if mongo_record == None:
        logging.warning(f"Mongo Record for {primary_key}: {ref_id} was not found.")
        return
    return mongo_record

def mongo_get_many(primary_key, ref_id, collection):
    mongo_records = collection.find({primary_key:ref_id})
    if mongo_records == None:
        logging.warning(f"Mongo Record for {primary_key}: {ref_id} was not found.")
        return
    return mongo_records

def mongo_set(primary_key,ref_id,collection,insert_document,overwrite=False):
    mongo_record = collection.find_one({primary_key:ref_id})
    mongo_id = mongo_record[primary_key] if mongo_record != None else None
    if mongo_id == None: 
        logging.info(f"Mongo ID ({ref_id}) not found in collection. record will be created.")
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
        logging.warning(f"no update/insert made. record for '{mongo_id}' already exists and Overwrite == False.")
        return
    logging.info("Updating actions completed")
    return


def mongo_set_many(
        primary_key:str,
        collection:str,
        insert_documents: list[dict],
        overwrite=False,
    ) -> None:

    logging.info(f"Command to bulk write to {collection}: {len(insert_documents)} records.")

    # Create Requests bank
    requests = []
    
    # if the requests are set to overwrite, instantiate ReplaceOne jobs
    if overwrite:
        for doc in insert_documents:
            ref_id = doc[primary_key]
            requests.append(
                ReplaceOne(
                    filter={primary_key:ref_id},
                    replacement=doc,
                    upsert=True,
                    )
                ) 
            
    # if no overwrite, only create InsertJobs
    else: requests += [InsertOne(document=doc) for doc in insert_documents]
    
    result = collection.bulk_write(requests)
    logging.info(f"Inserted Count: {result.inserted_count} // Deleted Count: {result.deleted_count} // Modified Count: {result.modified_count}")

    return 


def mongo_delete(primary_key, ref_id, collection):
    if ref_id == None:
        logging.warning("No referenece ID provided, skipping delete")
        return
    mongo_record = collection.find_one({primary_key:ref_id})
    mongo_record_item = mongo_record[primary_key] if mongo_record != None else None
    count = collection.delete_many({primary_key:mongo_record_item}).delete_count
    if count <= 0 or count == None:
        logging.warning("No records deleted from collection")
    else:
        logging.info(f"Mongo record {primary_key}: {mongo_record_item} removed from Collection.")
    return