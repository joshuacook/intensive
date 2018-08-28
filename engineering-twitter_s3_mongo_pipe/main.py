from datetime import datetime
import json
from os import rename

from s3 import create_boto_client, process_local_file_to_S3
from twitter_funcs import collect_tweets, create_tweet_iterator
from mongo import create_mongo_client_to_database_collection, insert_to_mongo
from utility import get_credentials, timestamp, write_to_disk
from requests import HTTPError

if __name__ == "__main__":

    credentials = get_credentials()
    if credentials['twitter']['token'] is None:
        print("Did you forget to add your twitter tokens to the credentials.json file?")
        raise HTTPError

    tweet_iterator    = create_tweet_iterator()
    s3_client         = create_boto_client()
    collection_client = create_mongo_client_to_database_collection()

    while True:
        timestamp()
        tweets   = collect_tweets(tweet_iterator, 100)
        filename = write_to_disk(tweets)
        process_local_file_to_S3(s3_client,filename)
        insert_to_mongo(s3_client, collection_client, filename)
