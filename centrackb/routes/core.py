"""
Routes and views for the bottle application.
"""
import sys
import logging
from datetime import datetime, date
from bottle import HTTPError, post, route, request, response, redirect,\
     error, static_file, view as viewb, HTTPResponse
from requests.exceptions import ConnectionError

import db
import utils
from utils import get_session, write_log, get_weekdate_bounds, view,\
     _get_ref_date, Storage as _
from services import api, choices, stats, transform, report
from settings import FMT_SHORTDATE, NL_PAGE_SIZE
from routes import authnz, authorize
from forms import CaptureForm, PasswordChangeForm



@route('/')
@view('index')
def index():
    #+==========================
    #: forms series summary
    records = []
    projects = db.Project.get_all()
    ref_date = _get_ref_date()
    wkdate_bounds = get_weekdate_bounds

    for p in projects:
        record = _(id=p.id, name=p.name)
        captures = db.Capture.get_by_project(p.id, paginate=False)
        if captures.count():
            summary = stats.series_purity_summary(captures, ref_date)
            record.update(summary)
        records.append(record)

    #+==========================
    #: today activity summary
    activity_summary, activity_stats = [], _()
    captures = list(db.Capture.get_by_date(ref_date.isoformat(), paginate=False))
    if captures:
        activity_stats = stats.day_activity_stats(captures, ref_date)
        activity_breakdown = stats.day_activity_breakdown(captures, ref_date)
        for record in activity_breakdown:
            activity_summary.append(_(record))

    return {
        'is_front': True, 
        'title': 'Capture Summary',
        'records': records,
        'activity_records': activity_summary,
        'activity_stats': activity_stats,
        'report_ref_date': ref_date,
        'report_weekdate_bounds': wkdate_bounds,
    }

@route('/profile', method=['GET', 'POST'])
@view('profile')
@authorize()
def profile():
    user = authnz.current_user
    user_info = _(username=user.username,
                  email_addr=user.email_addr,
                  role=user.role)
    
    session = get_session()['messages']
    if request.method == 'POST':
        form = PasswordChangeForm(request, user)
        try:
            if form.is_valid():
                form.save()
                session['pass'].append('Password has been changed successfully.')
                return authnz.logout(success_redirect='/profile')
            else:
                session['fail'].append(form.errors)
        except HTTPResponse:
            raise
        except Exception as ex:
            error_message = 'Password change failed. Error: %s' % str(ex)
            session['fail'].append(error_message)
            logging.error(error_message, exc_info=True)
    
    roles = sorted(
        list(authnz.list_roles()),
        key=lambda x: x[1], reverse=True)
    return {
        'title': 'Profile',
        'user': user_info,
        'roles': roles,
        'readonly': True,
    }


@route('/projects/')
@view('projects')
def projects():
    records = []
    projects = db.Project.get_all()

    for p in projects:
        record = _(id=p.id, name=p.name)
        captures = db.Capture.get_by_project(p.id, paginate=False)
        if captures.count():
            summary = stats.activity_summary(captures)
            record.update(summary)
        records.append(record)

    return {
        'title': 'Projects',
        'records': records
    }


@route('/projects/<project_id>/')
@view('project-view')
@authorize()
def project_view(project_id):
    project = db.Project.get_by_id(project_id)
    xrecords, urecords = [], []

    for f in project.xforms:
        xform = db.XForm.get_by_id(f)
        record = _(id=xform.id_string, title=xform.title)
        captures = db.Capture.get_by_form(f, False)
        if captures.count():
            summary = stats.activity_summary(captures)
            record.update(summary)
        xrecords.append(record)

    for f in project.uforms:
        uform = db.XForm.get_by_id(f)
        record = _(id=uform.id_string, title=uform.title)
        updates = db.Update.get_by_form(f, False)
        if updates.count():
            summary = stats.activity_summary(updates)
            record.update(summary)
        urecords.append(record)

    return {
        'title': 'Project: %s' % project.name,
        'project': project,
        'xrecords': xrecords,
        'urecords': urecords
    }


@post('/projects/<project_id>/sync')
@authorize(role='moderator')
def project_sync(project_id):
    p = db.Project.get_by_id(project_id)
    if not p:
        raise HTTPError(404, 'Project not found: %s' % project_id)

    messages = get_session()['messages']
    form_type, xforms_to_sync = None, None
    for key in ['project_xforms', 'project_uforms']:
        if key in request.forms:
            form_type = key
            xforms_to_sync = request.forms.get(key).split(',')

    sync_target = (db.Capture if form_type == 'project_xforms' else db.Update)

    # get form count
    for xform_id in xforms_to_sync:
        count = sync_target.count_by_form(xform_id)
        xform = db.XForm.get_by_id(xform_id)

        # pull new captures
        try:
            transformed, pull_count = [], 0
            for captures in api.get_captures(xform.id, start=count):
                logging.debug('# captures pulled: %s', len(captures))
                if captures:
                    pull_count += len(captures)
                    for c in captures:
                        transformed.append(transform.to_flatten_dict(c))

                    sync_target.save_many(transformed)
                    transformed = []

            messages['pass'].append('%s captures pulled.' % pull_count)
        except ConnectionError:
            messages['fail'].append('Sync failed. Internet connection required.')
        except Exception as ex:
            messages['fail'].append('Sync failed. %s' % str(ex))
            logging.error('sync failed. %s', str(ex), exc_info=True)

    return redirect('/projects/%s/' % project_id)


@route('/xforms/<form_id>/')
@view('xform-capture-summary')
def xform_info(form_id):
    xform = db.XForm.get_by_id(form_id)
    captures = db.Capture.get_by_form(form_id, paginate=False)
    summaries = stats.summary_by_day(captures)

    return {
        'title': 'Daily Summary',
        'sync_records': [],
        'records': summaries,
        'xform': xform
    }


@post('/r/default/')
@authorize(role='moderator')
def report_default():
    messages = get_session()['messages']

    project_id = request.forms.get('project_id')
    ref_date = request.forms.get('ref_date')

    try:
        result = report.write_report(project_id, ref_date)
        # messages['pass'].append('Report generated.')
        return static_file(result[0], root=result[1], download=True)
    except Exception as ex:
        messages['fail'].append('Report generation failed. %s' % str(ex))
        print(ex)
    return redirect('/')


@route('/captures/')
@view('capture-list')
def capture_list():
    result = _query_capture(
        tbl = db.Capture,
        title = 'Captures',
        item_id=None )
    result['has_duplicates'] = _query_duplicate_count('captures')
    result['has_updates'] = _query_updates_count
    return result


@route('/captures/<item_id:int>/')
@view('capture-view')
@authorize(role='team-lead')
def capture_view(item_id):
    r = _query_capture(
            tbl=db.Capture, 
            title='Capture Item', 
            item_id=item_id)
    
    # retrieve duplicates
    qry_dup = {'_id': {'$ne': item_id}, 
              'rseq': r['record']['rseq']}
    
    cur = db.Capture.query(paginate=False, **qry_dup)
    r['duplicates'] = [_(item) for item in cur]
    
    # retrieve updates
    qry_upd = {'rseq': r['record']['rseq']}
    cur = db.Update.query(paginate=False, **qry_upd)
    r['updates'] = [_(item) for item in cur]
    r['record_type'] = 'captures'
    return r


@route('/updates/')
@view('capture-list')
def update_list():
    result = _query_capture(
        tbl=db.Update,
        title='Updates',
        item_id=None)
    result['has_duplicates'] = _query_duplicate_count('updates')
    
    # fix: Issue #7 [local-gogs]
    # manually update the ids for projects to be returned
    project_choices = []
    for (_id, name) in result['project_choices']:
        project_choices.append((_id.replace('_cf_', '_cu_'), name))
    
    result['project_choices'] = project_choices
    return result


@route('/updates/<item_id:int>/')
@view('capture-view')
@authorize(role='team-lead')
def update_view(item_id):
    r = _query_capture(
            tbl=db.Update,
            title='Update Item',
            item_id=item_id)
    
    # retrieve duplicates
    qr_dup = {'_id': {'$ne': item_id},
              'rseq': r['record']['rseq']}
    
    cur = db.Update.query(paginate=False, **qr_dup)
    r['duplicates'] = [_(item) for item in cur]
    r['record_type'] = 'updates'
    return r


@route('/export/<record_type:re:(captures|updates)>/')
@view('export_result')
def export_captures(record_type):
    import os, csv
    from settings import REPORTS_DIR, report_cols
    
    table = (db.Capture if record_type == 'captures' else db.Update)
    resp = _query_capture(table, None, None, False)
    
    filename = '%s-export@%s.csv' % (record_type, datetime.today().strftime('%Y%m%dT%H%M'))
    filepath = os.path.join(REPORTS_DIR, filename)
    extract = lambda r: {k: r.get(k, '-') for k in report_cols}
    
    dialect = csv.excel
    dialect.lineterminator = '\r'
    
    status, error = 'Unknown', ''
    try:
        with open(filepath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=report_cols, dialect=dialect)
            writer.writeheader()
            for record in resp['records']:
                writer.writerow(extract(record))
            
            csvfile.flush()
            status = 'Success'
        
        return static_file(filename, root=REPORTS_DIR, download=True)
    except Exception as ex:
        logging.error('Export failed. Error: %s', str(ex), exc_info=True)
        os.remove(filepath)
        status = 'Failed'
        error = str(ex)
    return {
        'title': 'Export Result', 'status': status, 
        'filename': filename, 'error': error
    }


def _query_capture(tbl, title, item_id, paginate=True):
    if not item_id:
        # handle query parameters here
        query, sorts, q = {}, {}, request.query.get('q')
        duplicate_field = None
        if q:
            search = {'$regex': '.*%s.*' % q, '$options':'i'}
            query = {'$or': [
                {'enum_id': search },
                {'rseq': search },
                {'cust_name': search },
                {'acct_status': search},
                {'acct_no': search},
                {'tariff': search},
                {'meter_type': search},
                {'datetime_today': search},
            ]}
        else:
            query = {}
            filter_fields = ['datetime_today','enum_id','rseq','acct_status',
                             'acct_no', 'meter_status','meter_type',
                             'project_id', 'show_duplicate']
            
            for f in filter_fields:
                entry = request.query.get(f, None)
                if entry:
                    if f != 'show_duplicate':
                        query[f] = {'$regex': '.*%s.*' % entry, '$options':'i'}
                    else:
                        duplicate_field = entry
            
            sort_fields = ['sort_by', 'then_by']
            for sf in sort_fields:
                entry = request.query.get(sf, None)
                if entry:
                    sorts[sf] = entry

        # data to retrieve
        page = tbl.query(paginate=paginate, sort_by=list(sorts.values()), 
                         duplicate_field=duplicate_field, **query)
        
        # update so filter_query form state is restored
        query.update(sorts)
        if duplicate_field:
            query['show_duplicate'] = duplicate_field
            
        # extract project choices
        if not utils._PROJECTS_CHOICES_CACHE:
            project_choices = []
            for p in db.Project.get_all(False, paginate=False):
                project_choices.append((p['id'], p['name']))
            utils._PROJECTS_CHOICES_CACHE = project_choices
        
        
        return {
            'title': title,
            'records': page,
            'search_text': q,
            # select choices for the filter form
            'filter_params': _(query),
            'acct_status_choices': choices.ACCT_STATUS,
            'meter_type_choices': choices.METER_TYPE,
            'meter_status_choices': choices.METER_STATUS,
            'tariff_choices': choices.TARIFF,
            'duplicate_choices': choices.DUPLICATES,
            'project_choices': utils._PROJECTS_CHOICES_CACHE,
        }
    else:
        query = {}
        record = tbl.get(item_id)
        return {
            'title': title,
            'record': record,
        }


def _query_duplicate_count(table_name):
    def wrapper(record_id, rseq):
        result = db.db[table_name]\
                   .count({'_id': {'$ne': record_id}, 
                           'rseq': rseq,
                           '$or': [
                                {'dropped': False},
                                {'dropped': {'$exists': False}}
                            ]})
        return result
    return wrapper


def _query_updates_count(record_id, rseq):
    result = db.db.updates.count({'_id': {'$ne': record_id}, 'rseq': rseq})
    return result


# custom error pages

if '--debug' not in sys.argv:
    @error(code=404)
    @error(code=500)
    @viewb('error/page.tpl')
    def custom_error_handler(http_error):
        context = {
            'title': 'CENTrak : Error',
            'year': datetime.now().year,
        }
        
        status_code = http_error.status_code
        context['header'] = http_error.status_code
        if status_code == 404:
            context['message'] = 'Oooops! Requested resource was not found!'
        elif status_code == 500:
            context['message'] = (
                'An internal server error just occurred. Should this error '
                'persist, please contact the administrator and report this '
                'issue.')
        return context

