import os
import pandas as pd
from datetime import datetime

import db
from services import stats
from settings import BASE_DIR, KEDAT_DIR, report_cols



REPORT_DIR = os.path.join(KEDAT_DIR, '..', '_reports')
if not os.path.exists(REPORT_DIR):
    os.makedirs(REPORT_DIR)


def _norm(df):
    if df.index.size:
        columns = ['rseq', 'enum_id']
        for col in columns:
            df[col] = df[col].apply(lambda x: str(x).upper())
    return df


def get_duplicate_rseq(df):
    key, result = 'rseq', pd.DataFrame()
    d = df[df.duplicated(key) == True]
    
    for value in d[key].values:
        result = result.append(df[df[key] == value][report_cols])

    if result.index.size:
        result = result.sort(['rseq'], ascending=[1])
    return result


def get_duplicate_accts(df):
    key, result = 'acct_no', pd.DataFrame()
    f = df[df[key].isnull() == False]
    d = f[f.duplicated(key) == True]

    for value in d[key].values:
        result = result.append(df[df[key] == value][report_cols])

    if result.index.size:
        result = result.sort(['acct_no'], ascending=[1])
    return result


def get_activity_breakdown(df):
    summary = stats._activity_breakdown(df)

    # reshape results
    cols_order = [
        'group', 'upriser', '_total', '_rseq_duplicates', '_acctno_duplicates',
        'new', 'active', 'inactive', 'unknown', 'analogue', 'ppm', 'none']
        
    groups, rows = ([], [])
    for r in summary:
        grow = [r[c] for c in cols_order]
        groups.append(grow)
        rows.append(grow)

        for ir in r['uprisers']:
            irow = [ir[c] for c in cols_order]
            rows.append(irow)

    padding = [['']*len(cols_order) for i in range(3)]
    all = groups + padding + [cols_order[:]] + rows
    return pd.DataFrame(all, columns=cols_order)


def get_activity_by_day(df):
    summary = stats._activity_by_day(df)

    # reshape results
    cols_order = [
        'date', '_total', '_rseq_duplicates', '_acctno_duplicates',
        'new', 'active', 'inactive', 'unknown', 'analogue', 'ppm', 'none']
        
    rows = []
    for r in summary:
        row = [r[c] for c in cols_order]
        rows.append(row)

    return pd.DataFrame(rows, columns=cols_order)


def get_notes(ref_date):
    date_digits = ref_date.replace('-','')
    rows = [
        ['', '', ''],
        ['', 'SHEET-NAME', 'CONTENT DESCRIPTION'],
        ['', 'summary-by-day', 'All captures summarized day-by-day.'],
        ['', 'activity-so-far', 'All captures summarized by group by upriser.'],
        ['', 'dup-rseq-all', 'All duplicate route-seq. found across all captures'],
        ['', 'dup-acct-all', 'All duplicate acct. nos. found across all captures'],
        ['', 'activity-%s' % date_digits, 'Captures made %s summarized by group by upriser' % ref_date],
        ['', 'dup-rseq-%s' % date_digits, 'Duplicate route-seq. found across captures made %s' % ref_date],
        ['', 'dup-acct-%s' % date_digits, 'Duplicate route. nos. found across captures made %s' % ref_date],
        ['', 'group-a-%s' % date_digits, 'Captures made by Group-Alpha on %s' % ref_date],
        ['', 'group-b-%s' % date_digits, 'Captures made by Group-Bravo on %s' % ref_date],
        ['', 'group-c-%s' % date_digits, 'Captures made by Group-Charlie on %s' % ref_date],
        ['', 'group-d-%s' % date_digits , 'Captures made by Group-Delta on %s' % ref_date],
        ['', 'group-e-%s' % date_digits, 'Captures made by Group-Echo on %s' % ref_date],
        ['', '', ''],
        ['', 'HINT:', ''],
        ['', "The sn field can be used to track the same rows across all worksheets except the summary-by-day,", ''],
        ['', "acitivity-so-far and activity-<date> worksheets.", ''],
        ['', '', ''],
        ['', "The duplicate records within the dup-rseq-<date> and dup-acct-<acct> worksheets are meant to", ''],
        ['', "provide quick feedback on duplicates made on a given day. Corrections aren't to be effected on", ''],
        ['', "this worksheet. These records are equally available within the dup-rseq-all and dup-acct-all", ''],
        ['', "worksheets, the master worksheets.", ''],
        ['', '', ''],
        ['', "Team leads are expected to effect corrections on the master duplicate worksheets (dup-rseq-all", ''],
        ['', "and dup-acct-all). Records meant to be kept (the valid records) should be coloured green, while", ''],
        ['', "records to be delete should be coloured red. Team leads should only focus on correcting records", ''],
        ['', "provided by their team members, use the enum_id to track this, except when error cuts across", ''],
        ['', "team records.", ''],
    ]
    return rows


def write_report(project_id, ref_date):
    if not ref_date:
        ref_date = datetime.now().date().isoformat()

    date_digits = ref_date.replace('-','')
    fname = 'activity-report-%s.xls' % date_digits
    fpath = os.path.join(REPORT_DIR, fname)
    writer = pd.ExcelWriter(fpath)

    try:
        # write notes
        df = pd.DataFrame(get_notes(ref_date), columns=['','',''])
        df.to_excel(writer, 'notes', index=False)

        # begin captures analysis
        all_captures = db.Capture.get_by_project(project_id, False)
        df = pd.DataFrame(list(all_captures))

        # summarize activities by day
        summary = get_activity_by_day(df)
        summary.to_excel(writer, 'summary-by-day')

        # summarize all activities
        summary = get_activity_breakdown(df)
        summary.to_excel(writer, 'activity-so-far')
    
        # duplicate rseq all
        records = get_duplicate_rseq(df)
        records.to_excel(writer, 'dup-rseq-all')

        # duplicate acctno all
        records = get_duplicate_accts(df)
        records.to_excel(writer, 'dup-acctno-all')

        # summarize ref_date activity
        f = df[df['datetime_today'] == ref_date]
        if f['rseq'].size:
            summary = get_activity_breakdown(f)
            summary.to_excel(writer, 'activity-%s' % date_digits)
        
            records = get_duplicate_rseq(f)
            records.to_excel(writer, 'dup-rseq-%s' % date_digits)

            records = get_duplicate_accts(f)
            records.to_excel(writer, 'dup-acctno-%s' % date_digits)

            # captures summarized by groups
            gg = f.groupby('group')
            keys = sorted(gg.groups.keys())
        
            for key in keys:
                gf = gg.get_group(key)[report_cols]
                gf = _norm(gf).sort(['rseq'], ascending=[1])
                gf.to_excel(writer, 'group-%s-%s' % (key.lower(), date_digits))
    finally:
        writer.save()
    return (fname, REPORT_DIR)

