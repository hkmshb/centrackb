"""
Data access provider.
"""
import pymongo
from datetime import datetime
from bson.objectid import ObjectId

import utils
import settings
from utils import Storage as _



# connection
conn = pymongo.MongoClient()
db = conn[settings.MONGODB_NAME]


# utility functions
def get_station_name(code):
    if not utils._STATION_NAMES_CACHE:
        utils._STATION_NAMES_CACHE = {}
    
    code = (code or '').upper()
    if code and code not in utils._STATION_NAMES_CACHE:
        entry, station = {}, Station.get_by_code(code)
        if not station:
            entry.update({'name': '?', 'source_feeder': '?'})
        else:
            entry.update({
                'name': station.name, 
                'source_feeder': station.source_feeder
            })
        utils._STATION_NAMES_CACHE[code] = entry
    
    entry = utils._STATION_NAMES_CACHE[code]
    return entry['name']


# voltage ratios
class Volt:
    MVOLTL_LVOLT = 1
    MVOLTH_LVOLT = 2

    class Text:
        MVOLTL_LVOLT = '11/0.415KV'
        MVOLTH_LVOLT = '33/0.415KV'

    CHOICES = (
        (MVOLTL_LVOLT, Text.MVOLTL_LVOLT),
        (MVOLTH_LVOLT, Text.MVOLTH_LVOLT),
    )


class Project:
    
    @staticmethod
    def count():
        return db.projects.count({})

    @staticmethod
    def get_all(include_inactive=True, paginate=True):
        qry = {} if include_inactive else {'active': True}
        cur = db.projects.find(qry)\
                .sort('id', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def get_by_id(id):
        record = db.projects.find_one({'id': id})
        return _(record or {})

    @staticmethod
    def insert_one(record):
        tdy = datetime.today().date().isoformat()
        record['date_created'] = tdy
        record['last_modified'] = None
        return db.projects\
                 .insert_one(record)
    
    @staticmethod
    def set_active(id, status):
        tdy = datetime.today().date().isoformat()
        return db.projects\
                 .update_one(
            {'id': id},
            {'$set': {
                'active': status,
                'last_modified': tdy}
            }
        )
    
    @staticmethod
    def update_one(record):
        tdy = datetime.today().date().isoformat()
        record['last_modified'] = tdy
        return db.projects\
                 .update({'id': record.id}, record)


class XForm:

    @staticmethod
    def count(include_inactive=False):
        qry = {} if include_inactive else {'active': True}
        return db.xforms.count(qry)

    @staticmethod
    def get_all(include_inactive=False, paginate=True):
        qry = {} if include_inactive else {'active': True}
        cur = db.xforms.find(qry)\
                .sort('id', pymongo.DESCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def get_unassigned_xforms(include_inactive=False, paginate=True):
        xforms = []
        for p in Project.get_all(paginate=False):
            xforms.extend(p['xforms'])

        qry = {'id': {'$nin': xforms}}
        if not include_inactive:
            qry.update({'active': True})

        cur = db.xforms.find(qry)\
                .sort('id', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def get_unassigned_uforms(include_inactive=False, paginate=True):
        uforms = []
        for p in Project.get_all(paginate=False):
            uforms.extend(p['uforms'])
        
        # HACK: included the cust_updform regex pattern to support update
        # forms used for Hotoro 11KV Feeder...
        qry = {
            'id': {'$nin': uforms}, 
            'id_string': {'$regex': '(f[0-9]{3}_cu.+|cust_updform.+)'}
        }
        if not include_inactive:
            qry.update({'active': True})

        cur = db.xforms.find(qry)\
                .sort('id', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur
  
    @staticmethod
    def get_by_id(id):
        record = db.xforms.find_one({'id_string': id })
        return _(record or {})

    @staticmethod
    def insert_one(record):
        tdy = datetime.today().date().isoformat()
        record['date_created'] = tdy
        record['last_modified'] = None
        return db.xforms\
                 .insert_one(record)
    
    @staticmethod
    def set_active(id, status):
        tdy = datetime.today().date().isoformat()
        return db.xforms.update_one(
            {'id_string': id},
            {'$set': {
                'active': status,
                'last_modified': tdy }
            }
        )


class CaptureBase:
    
    def __init__(self, collection_name):
        self._collection_name = collection_name
    
    @property
    def db(self):
        return db[self._collection_name]
        
    def count_by_date(self, ref_date):
        return self.db\
                   .count({'datetime_today': ref_date})

    def count_by_date_form(self, ref_date, ref_id):
        return self.db\
                   .count({'datetime_today': ref_date,
                           '_xform_id_string': ref_id })
    
    def count_by_form(self, ref_id):
        return self.db\
                   .count({'_xform_id_string': ref_id})

    def count_by_project(self, project_id):
        return self.db\
                   .count({'project_id': project_id})

    def count_by_station(self, station_code):
        return self.db\
                   .count({'station': station_code})

    def get(self, _id):
        record = self.db.find_one({'_id': _id})
        return _(record or {})

    def get_by_rseq(self, rseq):
        record = self.db.find_one({'rseq': rseq})
        return _(record or {})

    def get_by_date(self, ref_date, paginate=True):
        cur = self.db\
                  .find({'datetime_today': ref_date})\
                  .sort('rseq', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    def get_by_date_form(self, ref_date, ref_id, paginate=True):
        cur = self.db\
                  .find({'datetime_today': ref_date,
                         '_xform_id_string': ref_id})
        return utils.paginate(cur) if paginate else cur

    def get_by_form(self, ref_id, paginate=True):
        cur = self.db\
                  .find({'_xform_id_string': ref_id})\
                  .sort((['datetime_today', pymongo.ASCENDING],
                         ['rseq', pymongo.ASCENDING]))
        return utils.paginate(cur) if paginate else cur

    def get_by_project(self, project_id, paginate=True):
        cur = self.db\
                  .find({'project_id': project_id})\
                  .sort('date_created', pymongo.DESCENDING)
        return utils.paginate(cur) if paginate else cur
    
    def get_available_updates(self, field, **params):
        from copy import deepcopy
        qry = ({} if not params else deepcopy(params))
        if 'project_id' in qry:
            value = qry['project_id']['$regex']
            qry['project_id']['$regex'] = value.replace('_cf_', '_cu_')
        
        cur = db.updates.find(qry, {'rseq': 1})
        rseqs = [r['rseq'] for r in cur]
        return rseqs
    
    def get_duplicates(self, field, **params):
        qry = ({} if not params else params.copy())
        if field == 'acct_no':
            qry.update({'acct_no': {'$ne': None}})
            
        aggregation = [
            {'$match': qry},
            {'$group': {'_id': '$%s' % field, 'total': {'$sum': 1}}},
            {'$match': {'total': {'$gt': 1}}}
        ]
        
        duplicates = []
        for r in self.db.aggregate(aggregation):
            duplicates.append(r['_id'])
        return (field, duplicates)
    
    def replace(self, record_id, new_record):
        self.db.update({'_id': record_id}, new_record)
    
    def query(self, project_id=None, form_id=None, include_dropped=False,
                paginate=True, sort_by=None, show_only_field=None, **params):
        qry = {}
        if project_id:
            qry.update({'project_id': project_id})
        if form_id:
            qry.update({'_xform_id_string': form_id})
        if not include_dropped:
            qry.update({'$or': [{'dropped': False}, {'dropped': {'$exists': False}}]})
        if params:
            qry.update(params)
        
        # check if to restrict filter to duplicates only
        if show_only_field:
            # note: showing dropped records only does and doesn't qualify as 
            # duplicate records depending on how you think about it... In this
            # case we consider all records marked as dropped as duplicate and
            # it helps answer the question 'what records have been dropped?'
            if show_only_field == 'dropped':
                qry.update({show_only_field: True})
                
                # if query already contain references to dropped records
                # purge that and have just this criteria included... 
                if qry.get('$or') and 'dropped' in str(qry.get('$or')):
                    del qry['$or']
            elif show_only_field == 'updated':
                qry.update({
                    'last_updated': {'$exists': 1}, 
                    'last_updated': {'$ne': None}
                })
            elif show_only_field == 'with-updates':
                # setup a mumbo-jumbo non-record returning query if the query
                # is run against the captures update table
                if self._collection_name == 'updates':
                    qry = {'rseq': '~!@#$%^&*()_+'}
                else:
                    _rseqs = self.get_available_updates(show_only_field, **qry)
                    qry.update({'rseq': {'$in': _rseqs}})
            else:
                duplicates = self.get_duplicates(show_only_field, **qry)
                qry = {show_only_field: {'$in': duplicates[1]}}
        
        cur = self.db.find(qry)
        if not sort_by:
            cur = cur.sort((['datetime_today', pymongo.DESCENDING],
                            ['group', pymongo.ASCENDING],
                            ['rseq', pymongo.ASCENDING]))
        else:
            sort_args = []
            for sort_arg in sort_by:
                sort_args.append([sort_arg, pymongo.ASCENDING])
            cur = cur.sort(sort_args)
        return utils.paginate(cur, size=settings.NL_PAGE_SIZE) if paginate else cur

    def save_many(self, records):
        self.db\
            .insert_many(records)


class UpdateBase(CaptureBase):

    def __init__(self):
        super(UpdateBase, self).__init__('updates')

    def insert_one(self, record):
        transform = self._transform(record)
        self.db\
            .insert_one(transform)

    def save_many(self, records):
        for record in records:
            self.insert_one(record)

    def _transform(self, record):
        return record


Capture = CaptureBase('captures')
Update = UpdateBase()


class Feeder:

    @staticmethod
    def count():
        return db.feeders.count({})

    @staticmethod
    def get_all(include_inactive=True, paginate=True):
        qry = {} if include_inactive else {'active': True}
        cur = db.feeders.find(qry)\
                .sort('code', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def get_by_code(code):
        record = db.feeders.find_one({'code': code.upper()})
        return _(record or {})

    @staticmethod
    def get_by_voltage(voltage, include_inactive=False, paginate=True):
        qry = {'voltage': voltage}
        if not include_inactive:
            qry.update({'active': True})
        cur = db.feeders.find(qry)\
                .sort('code', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def insert_one(record):
        tdy = datetime.today().date().isoformat()
        record['active'] = True
        record['date_created'] = tdy
        record['last_modified'] = None
        return db.feeders\
                 .insert_one(record)
     
    @staticmethod
    def update_one(record):
        tdy = datetime.today().date().isoformat()
        record['last_modified'] = tdy
        record._id = ObjectId(record._id)
        return db.feeders\
                 .update({'_id': record._id}, record)


class Station:

    @staticmethod
    def count():
        return db.stations.count({})

    @staticmethod
    def count_by_feeder(feeder_code):
        return db.stations\
                 .count({'source_feeder': feeder_code.upper()})

    @staticmethod
    def get_all(include_inactive=True, paginate=True):
        qry = {} if include_inactive else {'active': True}
        cur = db.stations.find(qry)\
                .sort('code', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def get_by_code(code):
        record = db.stations.find_one({'code': code.upper()})
        return _(record or {})

    @staticmethod
    def get_by_feeder(feeder_code, paginate=True):
        qry = {'source_feeder': feeder_code.upper()}
        cur = db.stations.find(qry)\
                .sort('code', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def get_by_category(category, include_inactive=False, paginate=True):
        qry = {'category': category.upper()}
        if not include_inactive:
            qry.update({'active':True})
        cur = db.stations.find(qry)\
                .sort('code', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def get_by_type(is_public, include_inactive=False, paginate=True):
        qry = {'public': is_public}
        if not include_inactive:
            qry.update({'active':True})
        cur = db.stations.find(qry)\
                .sort('code', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur

    @staticmethod
    def insert_one(record):
        tdy = datetime.today().date().isoformat()
        record['active'] = True
        record['date_created'] = tdy
        record['last_modified'] = None
        return db.stations\
                 .insert_one(record)
     
    @staticmethod
    def update_one(record):
        tdy = datetime.today().date().isoformat()
        record['last_modified'] = tdy
        record._id = ObjectId(record._id)
        return db.stations\
                 .update({'_id': record._id}, record)


class UserProfile:
    
    @staticmethod
    def get_all(paginate=True):
        qry = {}
        cur = db.user_profiles.find(qry)\
                .sort('id', pymongo.ASCENDING)
        return utils.paginate(cur) if paginate else cur
    
    @staticmethod
    def get_by_username(username):
        record = db.user_profiles.find_one({'username': username})
        return _(record or {})
    
    @staticmethod
    def insert_one(record):
        username = record.get('username')
        if not username:
            raise Exception('UserProfile must include username.')
        
        if db.user_profiles.count({'username': username}) != 0:
            msg_format = "UserProfile with username `%s` already exists."
            raise Exception(msg_format % username)
        
        db.user_profiles.insert_one(record)
    
    @staticmethod
    def update_one(record):
        username = record.get('username')
        if not username:
            raise Exception('UserProfile must include username.')
        
        db.user_profiles.update_one({'username': username}, record)
    
    @staticmethod
    def delete_one(username):
        db.user_profile.delete({'username': username})

