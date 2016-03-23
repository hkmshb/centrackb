"""
Routes and views for admin access.
"""
from bottle import HTTPError, post, route, request, redirect, HTTPResponse
from requests import ConnectionError
import pymongo
import logging

from utils import view, get_session, Storage as _
from routes import authnz, authorize
from services import api, imxport
import db, forms, utils



def _get_vratio_display(vratio_id):
    for i, text in db.Volt.CHOICES:
        if vratio_id == str(i):
            return text
    return None


@route('/admin/')
@view('admin/index')
@authorize(role='moderator')
def index():
    return {
        'title': 'Admin',
        'stat': _({
            'count_xforms': db.XForm.count(),
            'count_projects': db.Project.count()
        })
    }


@route('/admin/users/')
@view('admin/users')
@authorize(role='moderator')
def users():
    fields = ['username', 'role', 'email_addr', 'description']
    def func_users():
        for values in authnz.list_users():
            row = zip(fields, values)
            yield _(row)
    
    def func_pending():
        for code in authnz._store.pending_registrations:
            row = authnz._store.pending_registrations[code]
            yield _(row)
    
    return {
        'title': 'Users',
        'records': func_users(),
        'pending_records': func_pending()
    }


@route('/admin/users/<username>/', method=['GET', 'POST'])
@view('admin/user-form')
@authorize(role='moderator')
def manage_user(username):
    user = authnz.user(username)
    if not user:
        raise HTTPError(404, "User not found: %s" % username)
    
    user_info = _(username=user.username,
                  email_addr=user.email_addr,
                  role=user.role)
    
    session = get_session()['messages']
    if request.method == 'POST':
        form = forms.UserForm(request)
        try:
            if form.is_valid():
                form.save()
                session['pass'].append('User updated!')
                return redirect('/admin/users/')
            else:
                session['fail'].append(form.errors)
        except HTTPResponse:
            raise
        except Exception as ex:
            session['fail'].append('User update failed. Error: %s' % str(ex))
            
        # reflect/retain user changes
        user_info.update({
            'email_addr': request.forms.get('email_addr', ''),
            'role': request.forms.get('role', ''),
        })
    
    roles = sorted(list(authnz.list_roles()), key=lambda x: x[1], reverse=True)
    return {
        'title': 'User',
        'user': user_info,
        'roles': roles,
        'readonly': False,
    }


@route('/admin/users/<username>/change_password', method=['POST'])
@authorize()
def change_user_password(username):
    user = authnz.user(username)
    if not user:
        raise HTTPError(404, "User not found: %s" % username)
    
    # moderators should not be able to change the admin's password
    authd_user = authnz.current_user
    if authd_user.role in ('admin', 'moderator'):
        if authd_user.role == 'moderator' and user.role == 'admin':
            return redirect('/restricted')
    
    # non-admin and non-moderators should only be able to change their own
    # password
    elif authd_user.role not in ('admin', 'moderator'):
        if authd_user.username != user.username:
            return redirect('/restricted')
    
    # go ahead and make za change...
    session = get_session()['messages']
    form = forms.PasswordChangeForm(request, user)
    try:
        if form.is_valid():
            form.save()
            session['pass'].append('Password has been changed successfully.')
            
            # end session if password changed for current user
            if authd_user.username == user.username:
                return authnz.logout(success_redirect=('/admin/users/%s/' % username))
        else:
            session['fail'].append(form.errors)
    except HTTPResponse:
        raise
    except Exception as ex:
        error_message = 'Password change failed. Error: %s' % str(ex)
        session['fail'].append(error_message)
        logging.error(error_message, exc_info=True)
        
    return redirect('/admin/users/%s/' % username)


@route('/admin/projects/')
@view('admin/projects')
@authorize(role='moderator')
def projects():
    def func(xforms):
        def f(id):
            for xf in xforms:
                if xf.id_string == id:
                    return xf.title
            return ''
        return f

    projects = db.Project.get_all(include_inactive=True)
    xforms = db.XForm.get_all(include_inactive=True)
    return {
        'title': 'Projects', 'records': projects,
        'get_xform_title': func(xforms),
    }


@route('/admin/projects/create', method=['GET', 'POST'])
@route('/admin/projects/<id>/', method=['GET', 'POST'])
@view('admin/project-form')
@authorize(role='moderator')
def manage_project(id=None):
    project = _(xforms=[], uforms=[]) if not id else db.Project.get_by_id(id)
    if not project:
        raise HTTPError(404, "Project not found: %s" % id)

    xforms = db.XForm.get_unassigned_xforms(False, False)
    uforms = db.XForm.get_unassigned_uforms(False, False)
    session = get_session()
        
    if request.method == 'POST':
        form = forms.ProjectForm(request)
        try:
            if form.is_valid():
                form.save()
                action = ('created' if not id else 'updated')
                session['messages']['pass'].append('Project %s' % action)
                
                # HACK: clear cache used by capture/update listing
                utils._PROJECTS_CHOICES_CACHE = None
            else:
                session['messages']['fail'].extend(form.errors)

            return redirect('/admin/projects/')
        except pymongo.errors.DuplicateKeyError:
            session['messages']['fail'].append("Provided Project Id and/or Name already exists.")
            project = form._instance

    return {
        'title':'Projects',
        'project': project,
        'xforms': [_(f) for f in xforms],
        'uforms': [_(f) for f in uforms],
    }


@route('/admin/xforms/')
@view('admin/xforms')
@authorize(role='moderator')
def xforms():
    forms = db.XForm.get_all(include_inactive=True)
    return { 'title':'XForms', 'records': forms }


@post('/admin/xforms/sync')
@authorize(role='moderator')
def xforms_sync():
    failed, reports = [], []
    session = get_session()
    messages = session['messages']

    try:
        for forms in api.get_xforms():
            for f in forms:
                exist = db.XForm.get_by_id(f['id_string'])
                if exist: 
                    continue
        
                try:
                    f['active'] = False
                    db.XForm.insert_one(f)
                except Exception as ex:
                    failed.append(f)
                    reports.append(str(ex))

        if not failed:
            messages['pass'].append('Sync was successful.')
        else:
            all_failed = (len(forms) - len(failed)) == 0
            if all_failed:
                messages['fail'].append('Sync was unsuccessful.')
            else:
                msg = 'Sync was partially successful. %s entries failed.'
                messages['warn'].append(msg % len(failed))

            write_log(reports)
    except ConnectionError as ex:
        messages['fail'].append('Connection Error. Unable to establish '
                                'Internet connection.')
    return redirect('/admin/xforms/')


@post('/admin/xforms/update')
@authorize(role='moderator')
def xforms_update():
    active = request.forms.getall('activate')
    startup_all = request.forms.get('startup-all').split(',')
    startup_active = request.forms.get('startup-active').split(',')

    updated = []

    # handle recently activated forms
    new_actives = [x for x in active if x not in startup_active]
    for id in new_actives:
        db.XForm.set_active(id, True)
        updated.append(id)

    # handle recently deactivated forms
    inactives = [x for x in startup_all if x not in active]
    startup_inactives = [x for x in startup_all if x not in startup_active]
    new_inactives = [x for x in inactives if x not in startup_inactives]
    for id in new_inactives:
        print(db.XForm.set_active(id, False))
        updated.append(id)

    if updated:
        session = get_session()
        session['messages']['pass'].append('%s XForm(s) Updated.' % len(updated))
        session.save()
    return redirect('/admin/xforms/')


@route('/admin/feeders/')
@view('admin/feeders')
@authorize(role='moderator')
def feeders():
    feeders = db.Feeder.get_all(include_inactive=True)
    return {
        'title': 'Feeders', 
        'records': feeders,
        'get_station_count': db.Station.count_by_feeder,
        'get_capture_count': db.Capture.count_by_project
    }


@route('/admin/feeders/<code>/stations/')
@route('/admin/feeders/<code>/')
@view('admin/feeder-view')
@authorize(role='moderator')
def feeder_view(code):
    feeder = db.Feeder.get_by_code(code)
    stations = db.Station.get_by_feeder(code)
    return {
        'title': 'Feeder',
        'feeder': feeder,
        'stations': stations,
        'get_vratio_display': _get_vratio_display,
        'get_capture_count': db.Capture.count_by_station
    }


@route('/admin/feeders/create', method=['GET', 'POST'])
@route('/admin/feeders/<code>/edit', method=['GET', 'POST'])
@view('admin/feeder-form')
@authorize(role='moderator')
def manage_feeder(code=None):
    feeder = _() if not code else db.Feeder.get_by_code(code)
    if code and not feeder:
        raise HTTPError(404, "Feeder not found: %s" % id)

    session = get_session()        
    if request.method == 'POST':
        form = forms.FeederForm(request)
        try:
            if form.is_valid():
                form.save()
                action = ('created' if not code else 'updated')
                session['messages']['pass'].append('Feeder %s' % action)
            else:
                session['messages']['fail'].extend(form.errors)

            return redirect('/admin/feeders/')
        except pymongo.errors.DuplicateKeyError:
            session['messages']['fail'].append("Provided Feeder Code and/or Name already exists.")
            feeder = form._instance

    return {
        'title':'Projects',
        'feeder': feeder,
    }


@route('/admin/stations/<category>/')
@route('/admin/stations/')
@view('admin/stations')
@authorize(role='moderator')
def stations(category=None):
    category = category.upper() if category else 'I'
    if category not in ('I', 'D'):
        return redirect('/admin/stations/')

    title_prefix, feeder_voltage = 'Injection', '33'
    if category != 'I':
        title_prefix = 'Distribution'
        feeder_voltage = '11'

    stations = db.Station.get_by_category(category, include_inactive=False)
    feeders = db.Feeder.get_by_voltage(feeder_voltage, False, False)
    _cache, _name_format = {}, "%sKV %s"

    def _get_feeder_name(code):
        if code not in _cache:
            for f in feeders:
                _cache[f['code']] = _name_format % (f['voltage'], f['name'])
        return _cache.get(code, '')

    return {
        'title': '%s Stations' % title_prefix,
        'station_type': category,
        'records': stations,            
        'get_feeder_name': _get_feeder_name,
        'get_vratio_display': _get_vratio_display,
    }


@route('/admin/feeders/<feeder_code>/stations/create', method=['GET','POST'])
@route('/admin/feeders/<feeder_code>/stations/<code>/', method=['GET','POST'])
@view('admin/station-form')
@authorize(role='moderator')
def manage_station(feeder_code, code=None):
    feeder = db.Feeder.get_by_code(feeder_code)
    if not feeder:
        raise HTTPError(404, "Feeder not found: %s" % feeder_code)

    station = _() if not code else db.Station.get_by_code(code)
    if code and not station:
        raise HTTPError(404, "Station not found: %s" % code)

    session = get_session()['messages']
    if request.method == 'POST':
        form = forms.StationForm(request)
        try:
            if form.is_valid():
                form.save()
                action = ('created' if not code else 'updated')
                session['pass'].append('Station %s' % action)
            else:
                session['fail'].extend(form.errors)
            return redirect('/admin/feeders/%s/' % feeder_code)
        except pymongo.errors.DuplicateKeyError:
            session['fail'].append("Provided Station Code already exists.")
            station = form._instance
    
    return {
        'title': 'Station',
        'station': station,
        'feeder': feeder,
        'vratio_choices': db.Volt.CHOICES,
    }


@route('/admin/feeders/<feeder_code>/stations/import', method=['GET', 'POST'])
@view('admin/station-import')
def import_station(feeder_code):
    feeder = db.Feeder.get_by_code(feeder_code)
    if not feeder:
        raise HTTPError(404, "Feeder not found: %s" % feeder_code)

    session = get_session()['messages']
    if request.method == 'POST':
        form = forms.StationImportForm(request, '.csv')
        if form.is_valid():
            result = imxport.feeder_stations(feeder, form._instance.impfile)
            if not result.errors:
                session['pass'].append(result.summary())
            else:
                session['fail'].extend(result.errors)
            return redirect('/admin/feeders/%s/stations/' % feeder_code)
        else:
            session['fail'].extend(form.errors)

    return {
        'title': 'Import Feeder Stations'
    }


