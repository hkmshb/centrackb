"""
Provides access to the Survey platforms data via API.
"""
import json
from urllib.parse import urlencode

import requests
from settings import API_BASE_URL, AUTH_HEADER



def _qry2str(qry):
    return str(qry).replace("'", '"')


def get_xforms():
    try:
        url_base = API_BASE_URL % 'data'
        return _get(url_base, {})
    except Exception as ex:
        print('error (api.get_xform): %s' % str(ex))
        return []


def get_captures(form_id, date_captured=None, count=False, start=0):
    try:
        url_base = '%s/%s' % (API_BASE_URL % 'data', form_id)
        query = {}
        if date_captured:
            query = {"datetime_today": date_captured}

        return _get(url_base, query, count, start)
    except Exception as ex:
        print('error (api.get_captures): %s' % str(ex))
        return []


def _get(url_base, query, count=False, start=0, limit=100):
    def pull_list( start_at):
        params = {'start': start_at, 'limit':limit}
        if query:
            params.update({'query': _qry2str(query) })
        
        url = '%s?%s' % (url_base, urlencode(params))
        resp = requests.get(url, headers=AUTH_HEADER)
        return resp.json()

    def pull_scalar():
        params = {'count': 1}
        if query:
            params.update({'query': _qry2str(query)})

        url = '%s?%s' % (url_base, urlencode(params))
        resp = requests.get(url, headers=AUTH_HEADER)
        return len(resp.json())

    if count:
        return pull_scalar()
        
    data = pull_list(start)
    yield data

    while (len(data) == limit):
        start += limit
        data = pull_list(start)
        yield data
