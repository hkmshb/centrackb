import pandas as pd
from datetime import datetime

import db
import utils
from collections import OrderedDict
from kedat.core import Storage as _




def activity_summary(records):
    df = pd.DataFrame(list(records))
    return _activity_summary(df)


def series_purity_summary(records, ref_date=None):
    df = pd.DataFrame(list(records))
    result, key = _(), 'datetime_today'
    if not ref_date:
        ref_date = datetime.now().date()

    # today
    f = df[df[key] == ref_date.isoformat()]
    result.update(_purity_summary(f, 'd'))

    # week
    dates = utils.get_weekdate_bounds(ref_date)
    f = df[df[key] >= dates[0].isoformat()]
    f = f[f[key] <= dates[1].isoformat()]
    result.update(_purity_summary(f, 'w'))

    # month
    dates = utils.get_monthdate_bounds(ref_date)
    f = df[df[key] >= dates[0].isoformat()]
    f = f[f[key] <= dates[1].isoformat()]
    result.update(_purity_summary(f, 'm'))

    # all
    result.update(_purity_summary(df, ''))
    return result


def day_activity_breakdown(records, ref_date=None):
    df = pd.DataFrame(list(records))
    return _activity_breakdown(df)


def day_activity_stats(records, ref_date=None):
    df = pd.DataFrame(list(records))
    return _activity_stats(df)


def summary_by_day(records):
    df = pd.DataFrame(list(records))
    return _activity_by_day(df)


def _activity_by_day(df):
    results, key = [], 'datetime_today'
    if not df.index.size:
        return results
    
    # group records by date
    groups = df.groupby(key)
    gs = groups['rseq'].count()

    def _verbose(x):
        d = datetime.strptime(x, '%Y-%m-%d')
        return d.strftime('%Y-%m-%d : %a')

    for i in range(len(gs)):
        result = _(date=_verbose(gs.index[i]))
        
        # purity check
        gdf = groups.get_group(gs.index[i])
        result.update(_activity_summary(gdf))
        
        # collect results
        results.append(_(result))

    return results


def _activity_breakdown(df):
    results = []
    
    # group records by group-name
    ggroups = df.groupby('group')
    gs = ggroups['rseq'].count()

    for i in range(len(gs)):
        result = _(group=gs.index[i])

        # summaries
        gdf = ggroups.get_group(gs.index[i])
        result.update(_purity_summary(gdf, ''))
        result.update(_acct_status_summary(gdf))
        result.update(_meter_type_summary(gdf))

        #+===========================================:
        #: group by upriser
        ugroups = gdf.groupby('upriser')
        us = ugroups['rseq'].count()
        iresults = []
        result.uprisers = iresults

        for j in range(len(us)):
            iresult = _(upriser=us.index[j])
            
            # summaries
            udf = ugroups.get_group(us.index[j])
            iresult.update(_purity_summary(udf, ''))
            iresult.update(_acct_status_summary(udf))
            iresult.update(_meter_type_summary(udf))

            # collect results
            iresults.append(_(iresult))

        # collect result
        results.append(_(result))
    return results


def _activity_stats(df):
    result = _()

    # total captures
    result.capture_count = df.index.size
    
    # number of transformers & uprisers
    gdf = df.groupby('station')
    result.transformer_count = gdf['station'].count().index.size

    gdf = df.groupby('upriser')
    result.upriser_count = gdf['upriser'].count().index.size

    # number of devices used
    gdf = df.groupby('device_imei')
    result.device_count = gdf['device_imei'].count().index.size

    return result


def _activity_summary(df):
    result = _()
    result.update(_purity_summary(df, ''))
    result.update(_acct_status_summary(df))
    result.update(_meter_type_summary(df))
    return result


def _purity_summary(df, prefix):
    result, key = _(), 'datetime_today'
    result['%s_total' % prefix] = df.index.size

    # duplicate rseq check
    key = 'rseq'
    f = df[df.duplicated(key) == True]
    result['%s_rseq_duplicates' % prefix] = f.index.size

    # duplicate acct_no check
    key = 'acct_no'
    f = df[df[key].isnull() == False]
    f = f[f.duplicated(key) == True]
    result['%s_acctno_duplicates' % prefix] = f.index.size

    # fixed/updated records
    key = 'last_updated'
    f = df[df[key].isnull() == False]
    result['%s_updated' % prefix] = f.index.size
    return result


def _acct_status_summary(df):
    result, key = _(), 'acct_status'
    values = ['unknown', 'new', 'active', 'inactive', 'not-conn',
              'disconn-bill', 'disconn-no-bill', 'n_a']
    
    for value in values:
        f = df[df[key] == value]
        result[value.replace('-','_')] = f[key].size
    return result


def _meter_type_summary(df):
    result, key = _(), 'meter_type'
    values = ['none', 'analogue', 'ppm']
    
    for value in values:
        try:
            f = df[df[key] == value]
            result[value] = f[key].size
        except:
            result[value] = '-'
    return result

