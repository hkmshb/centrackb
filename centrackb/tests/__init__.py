import os
import json
import pymongo


BASE_DIR = os.path.dirname(__file__)
FIXT_DIR = os.path.join(BASE_DIR, 'fixtures')



def make_fixtures():
    db = pymongo.MongoClient().test_centrak
    cur = db.captures\
            .find({'datetime_today': '2016-01-08'})\
            .sort('enum_id', pymongo.ASCENDING)
    
    if not os.path.exists(FIXT_DIR):
       os.makedirs(FIXT_DIR)

    filepath = os.path.join(FIXT_DIR, 'captures-20160108.json')
    with open(filepath, 'w') as f:
        json.dump(list(cur), f, indent=2)
        f.flush()
    