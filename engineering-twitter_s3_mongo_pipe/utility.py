from datetime import datetime
import json

def create_timestamped_filename():

    credentials = get_credentials()
    username = credentials['username']
    timestamp_str = str(datetime.now())
    timestamp_str = (timestamp_str.replace(' ', '_')
                                  .replace('.', '-')
                                  .replace(':', '-'))
    filename = "tweets-" + username + '-' + timestamp_str + ".json"
    return filename

def get_credentials():
    with open("credentials.json", 'r') as stream:
        credentials = json.load(stream)
    return credentials

def timestamp():
    now = datetime.now().strftime('%D %H:%M:%S')
    print(now, end=' | ')
    print('Collecting Tweets', end=' | ')

def write_to_disk(tweets):
    filename = create_timestamped_filename()
    with open(filename, 'w') as outfile:
        json.dump(tweets, outfile)
    print('Written to Disk', end=' | ')
    return filename
