import pymongo
from redis import Redis
REDIS = Redis(host='this_redis')

def connect_to_mongo_and_reference_test_collections():
    mongo_client = pymongo.MongoClient(host='54.213.90.224',port=27016)
    database_ref = mongo_client.test_db
    collection_ref = database_ref.test_coll
    processed_coll_ref = database_ref.processed_test
    return collection_ref, processed_coll_ref

def pull_one_unprocessed_test_item(collection_ref):
    return next(collection_ref.find({'processed' : {'$exists': False}}))

def process_one_item(test_item, processed_coll_ref):
    
    this_processed_bar = test_item
    this_processed_bar['class'] = this_processed_bar['bar'] > 0.5
    processed_coll_ref.insert_one(this_processed_bar)
    
def update_test_item(collection_ref, test_item):
    collection_ref.update_one({'_id':test_item['_id']}, {'$set':{'processed':True}})
    
def pull_and_process_test_item():
    collection_ref, processed_coll_ref = connect_to_mongo_and_reference_test_collections()
    
    this_bar = pull_one_unprocessed_test_item(collection_ref)
    
    try:
        process_one_item(this_bar, processed_coll_ref)
    except pymongo.errors.DuplicateKeyError:
        pass
        
    
    update_test_item(collection_ref, this_bar)

    
    
    
def mapper(document):
    return [(word, 1) for word in (document
                                   .replace(',','')
                                   .replace('.','')
                                   .split())]

def collector(document, vocabulary):
    for token in mapper(document):
        REDIS.sadd(vocabulary, token[0])
        REDIS.rpush(*token)
        
def reducer(word):
    counts = [int(i) for i in REDIS.lrange(word, 0, -1)]
    return sum(counts)
    
    