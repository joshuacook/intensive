from pymongo import MongoClient
from s3 import read_object_from_S3
from utility import get_credentials

def create_mongo_client_to_database_collection():
    credentials = get_credentials()

    client = MongoClient(credentials['mongo']['ip'],
                         credentials['mongo']['port'])
    database = client.get_database(credentials['mongo']['database'])
    collection = database.get_collection(credentials['mongo']['collection'])
    print("Created Mongo Client")
    return collection

def insert_to_mongo(s3_client, collection_client, key):
    tweets_from_s3 = read_object_from_S3(s3_client, key)
    collection_client.insert_many(tweets_from_s3)
    print('Inserted to Mongo')
