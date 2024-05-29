from pymongo import MongoClient
import urllib 
import certifi
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)

import os 

MONGO_USER = os.getenv('mongoUser', 'mongoUser Path Not Found')
MONGO_PWD = os.getenv('mongoPwd', 'mongoPwd Path Not Found')

def open_apollo_db():
   uri = "mongodb+srv://%s:%s@apollodev.vha14oj.mongodb.net/?retryWrites=true&w=majority" % (MONGO_USER, urllib.parse.quote(MONGO_PWD))
   # Create a new client and connect to the server
   client = MongoClient(uri,tlsCAFile=certifi.where())
   # Send a ping to confirm a successful connection
   try:
      client.admin.command('ping')
      logging.info("pinged deployment. successfully connected to MongoDB.")
   except Exception as e:
      logging.error("Exception raise:")
      logging.error(e)
   return client

  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":     
   # Get the database
   dbname = open_apollo_db()
