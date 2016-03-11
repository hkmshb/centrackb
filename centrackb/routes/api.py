"""
Routes for API access.
"""
from datetime import datetime
from bottle import route, request, HTTPError
from utils import Storage as _

import db, forms
from routes import authnz, authorize


_CHOICES_CACHE = None



@route('/api/<record_type:re:(captures|updates)>/<record_id:int>/')
def captures(record_type, record_id):
    table = db.Capture if record_type == 'captures' else db.Update
    record = table.get(record_id)
    
    # del record['snapshots']         # exclude snapshots
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
    
    if not request.json:
        return {'success':False, 'message':'Posted record not available'}
    
    capture_upd, snapshot = _(request.json['capture']), None
    
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
    
    if not record.snapshots:
        snapshot = record.copy()
        del snapshot['snapshots']
    else:
        snapshot = record['snapshots']['original']['capture']
        
    # include audit details
    last_updated = datetime.today().strftime('%Y-%m-%d')
    capture_upd.last_updated = last_updated
    
    # include user details
    current_user = authnz.current_user
    capture_upd.updated_by = {
        'username': current_user.username,
        'email': current_user.email_addr,
        'role': current_user.role
    }
    
    # store snapshot of original data
    capture_upd.snapshots = {
        'original': {
            'capture': snapshot
        }
    }
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
        return 'Account deletion was successful!'
    except Exception as ex:
        return "Account deletion failed. Error: %s" % str(ex)


def _collect_choices():
    global _CHOICES_CACHE 
    if not _CHOICES_CACHE:
        from collections import OrderedDict
        from services import choices
        
        all = {
            'acct_status': OrderedDict(choices.ACCT_STATUS),
            'tariff': OrderedDict(choices.TARIFF),
            'tariff_new': OrderedDict(choices.TARIFF_NEW),
            'meter_type': OrderedDict(choices.METER_TYPE),
            'meter_brand': OrderedDict(choices.METER_BRAND),
            'meter_phase': OrderedDict(choices.METER_PHASE),
            'meter_status': OrderedDict(choices.METER_STATUS),
            'meter_location': OrderedDict(choices.METER_LOCATION),
            'plot_type': OrderedDict(choices.PLOT_TYPE),
            'supply_source': OrderedDict(choices.SUPPLY_SOURCE),
            'occupant': OrderedDict(choices.OCCUPANT),
            'addy_state': OrderedDict(choices.ADDY_STATE),
        }
        _CHOICES_CACHE = all
    return _CHOICES_CACHE
