import boto3
import json
from utility import create_timestamped_filename, get_credentials
from os import remove

def create_boto_client():
    s3 = boto3.resource('s3')

    credentials = get_credentials()

    client = boto3.client('s3',
                          aws_access_key_id=credentials['aws']['aws_access_key_id'],
                          aws_secret_access_key=credentials['aws']['aws_secret_access_key'])
    print("Created S3 Client")
    return client

def list_files_in_S3_bucket(client):

    credentials = get_credentials()
    s3_bucket = credentials['s3_bucket']

    objects = client.list_objects(Bucket=s3_bucket)
    objects_df = DataFrame(objects['Contents'])
    return list(objects_df.Key.values)

def process_local_file_to_S3(client, filename):
        write_file_to_S3(client, filename)
        remove(filename)
        print('Written to S3', end=' | ')

def read_object_from_S3(client, key):

    credentials = get_credentials()
    s3_bucket = credentials['s3_bucket']
    object_reference = client.get_object(Key=key,
                                         Bucket=s3_bucket)
    object_body = object_reference['Body']
    tweet_data = json.loads(object_body.read().decode())
    return tweet_data

def write_file_to_S3(client, filename):
    credentials = get_credentials()
    s3_bucket = credentials['s3_bucket']
    with open(filename) as infile:
        json_data=infile.read()
        client.put_object(Key=filename,
                          Body=json_data,
                          Bucket=s3_bucket)
