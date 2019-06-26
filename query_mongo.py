import datetime
import json
import pprint
from pymongo import MongoClient


client = MongoClient('localhost', 27017)


DB_NAME = 'lexicon'
COLLECTION_NAME = 'examples'

db = client[DB_NAME]
examples = db[COLLECTION_NAME]

eg = examples.find_one({'key-word':'action'})

print(eg)


#ex_id = '5d01f654a09ce8b25f89cf33'

#pprint.pprint(examples.find_one({"_id": ex_id}))