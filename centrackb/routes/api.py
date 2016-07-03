"""
Routes for API access.
"""
from datetime import datetime
from dateutil.parser import parse
from bottle import route, request, HTTPError
from utils import Storage as _

import db, forms
from routes import authnz, authorize


_CHOICES_CACHE = None
DATE_FIELDS    = ['datetime_start','datetime_end','datetime_today',
                  '_submission_time','last_updated','date_created']



@route('/api/<record_type:re:(captures|updates)>/<record_id:int>/')
def captures(record_type, record_id):
    table = db.Capture if record_type == 'captures' else db.Update
    record = table.get(record_id)
    
    # del record['snapshots']         # exclude snapshots
    # adjust datetime fields
    key, objs = 'snapshots', [record]
    if key in record and record[key] not in (None, {}):
        objs.append(record[key]['original']['capture'])
    
    for obj in objs:
        for f in DATE_FIELDS:
            if obj != record and f not in obj:
                continue
            value = obj[f]
            obj[f] = value.isoformat() if isinstance(value, datetime) else value
    
    result = {'capture': record}
    if not request.query.get('record_only', False):
        result.update({
            '_choices': _collect_choices(),
            '_meta': forms.CaptureForm._meta
        })
    return result


@route('/api/<record_type:re:(captures|updates)>/<record_id:int>/update', method=['POST'])
@authorize(role='team-lead')
def capture_update(record_type, record_id):
    table = db.Capture if record_type == 'captures' else db.Update
    record = table.get(record_id)
    if not record:
        return {'success':False, 'message':'Original record not found' }
    elif not request.json:
        return {'success':False, 'message':'Posted record not available'}
    
    capture_upd, snapshot = _(request.json['capture']), None
    if record_type == 'captures':
        # ensure user can make modification
        user = authnz.current_user
        profile = db.UserProfile.get_by_username(user.username)
        if user.role == 'team-lead' and profile.team.upper() != '_ALL_':
            user_team = profile.team.upper()[0]
            if user_team != record.enum_id.upper()[0]:
                msg = ("As team-lead for '%s' you cannot update capture entry "
                       "made by other teams besides yours.") % (profile.team)
                return {'success': False, 'message': msg}
        
        # if rseq changed ensure it doesn't cause duplication
        if record.rseq != capture_upd.rseq:
            assert record._id == capture_upd._id
            params = {'_id': {'$ne': capture_upd._id}, 'rseq': capture_upd.rseq}
            found = list(table.query(paginate=False, **params))
            if found and len(found) > 0:
                return {
                    'success':False, 
                    'message':(
                        'Update aborted. Capture with route sequence exist.\n'
                        'Existing Record (id=%s, enum_id=%s)' % (
                            found[0]['_id'], found[0]['enum_id']))
                }
        
        # if acct_no changed, ensure it doesn't cause duplication
        if record.acct_no != capture_upd.acct_no:
            assert record._id == capture_upd._id
    
            if capture_upd.acct_no == "" and capture_upd.acct_status == "new":
                if capture_upd.book_code == "":
                    return {
                        'success': False,
                        'message': "A new account is required to carry a 'Book Code'"
                    }
            else:
                params = {'_id': {'$ne': capture_upd._id}, 'acct_no': capture_upd.acct_no}
                found = list(table.query(paginate=False, **params))
                if found and len(found) > 0:
                    return {
                        'success': False,
                        'message': (
                            'Update aborted. Capture with account number exist.\n'
                            'Existing Record (id=%s, enum_id=%s)' % (
                                found[0]['_id'], found[0]['enum_id']))
                    }
        
        # store snapshot of original data
        key = 'snapshots'
        if not record.snapshots:
            snapshot = record.copy()
            if key in snapshot:
                del snapshot[key]
        else:
            snapshot = record[key]['original']['capture']
        capture_upd.snapshots = {'original': {'capture': snapshot}}
    
    ## all record types: captures, updates
    # include audit details
    capture_upd.last_updated = datetime.today()
    
    # include user details
    current_user = authnz.current_user
    capture_upd.updated_by = {
        'username': current_user.username,
        'role': current_user.role
    }
    
    # adjust datetime fields from string to datetime objects
    for f in DATE_FIELDS:
        value = capture_upd[f]
        capture_upd[f] = value if isinstance(value, datetime) else parse(value)
    
    table.replace(record_id, capture_upd)
    return {'success':True, 'message':'Record updated!'}


@route('/api/users/activate', method=['POST'])
@authorize(role='moderator')
def user_activate():
    code = request.POST.get('registration-code', '')
    try:
        authnz.validate_registration(code)
        return 'Account activation was successful!'
    except Exception as ex:
        return "Account activation failed. Error: %s" % str(ex)


@route('/api/users/<username>/delete', method=['POST'])
@authorize(role='moderator')
def user_deletion(username):
    try:
        authnz.delete_user(username)
        db.UserProfile.delete_one(username)
        return 'Account deletion was successful!'
    except Exception as ex:
        return "Account deletion failed. Error: %s" % str(ex)


@route('/api/registrations/<code>/delete', method=['POST'])
@authorize(role='moderator')
def registration_deletion(code):
    return "Yet to be impletemented!"


def _collect_choices():
    global _CHOICES_CACHE 
    if not _CHOICES_CACHE:
        from collections import OrderedDict
        from services import choices
        
        all = {
            'acct_status': OrderedDict(choices.ACCT_STATUS),
            'tariff': OrderedDict(choices.TARIFF),
            'tariff_pp': OrderedDict(choices.TARIFF_NEW),
            'meter_type': OrderedDict(choices.METER_TYPE),
            'meter_brand': OrderedDict(choices.METER_BRAND),
            'meter_phase': OrderedDict(choices.METER_PHASE),
            'meter_status': OrderedDict(choices.METER_STATUS),
            'meter_location': OrderedDict(choices.METER_LOCATION),
            'plot_type': OrderedDict(choices.PLOT_TYPE),
            'supply_source': OrderedDict(choices.SUPPLY_SOURCE),
            'occupant': OrderedDict(choices.OCCUPANT),
            'addr_state': OrderedDict(choices.ADDY_STATE),
        }
        _CHOICES_CACHE = all
    return _CHOICES_CACHE
