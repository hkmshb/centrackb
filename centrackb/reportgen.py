"""
Ad-hoc csv report generation script.
"""
import os, sys
import argparse
from datetime import datetime

import pandas as pd


BASE_DIR = os.path.dirname(__file__)
REPORT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '..', '..', '_reports'))

sys.path.append(os.path.join(BASE_DIR, '..', '..'))
import db


rpt_cols = ['datetime_today', 'rseq', 'enum_id', 'cust_name', 'addy_no', 
            'addy_street', 'acct_status', 'acct_no', 'tariff', 'cust_mobile1', 
            'cust_mobile2']

def get_duplicate_rseqs(df):
    key = 'rseq'
    d = df[df.duplicated(key) == True]
    duplicates = pd.DataFrame()
    for v in d[key].values:
        duplicates = duplicates.append(df[df[key] == v][rpt_cols])

    for col in rpt_cols:
        duplicates[col] = duplicates[col].apply(lambda x: str(x).upper())
    return duplicates


def get_duplicate_accts(df):
    key = 'acct_no'
    f = df[df[key].isnull() == False]
    d = f[f.duplicated(key) == True]
    
    duplicates = pd.DataFrame()
    for v in d[key].values:
        duplicates = duplicates.append(df[df[key] == v][rpt_cols])
    
    for col in rpt_cols:
        duplicates[col] = duplicates[col].apply(lambda x: str(x).upper())
    return duplicates


def get_invalid_stations(df, codes):
    if not codes:
        raise ValueError('Invalid codes not provided')
    
    key = 'station'
    df[key] = df['rseq'].apply(lambda x: x.upper().split('/')[0])
    records = pd.DataFrame()
    for v in [c.upper() for c in codes]:
        records = records.append(df[df[key] == v][[key] + rpt_cols])

    for col in ([key] + rpt_cols):
        records[col] = records[col].apply(lambda x: str(x).upper())
    return records


def get_records_by_upriser(upriser_code):
    query = {'rseq': {'$regex': '.*%s/*' % upriser_code, '$options':'i' }}
    captures = db.Capture.query(paginate=False, **query)
    df = pd.DataFrame(list(captures))

    result = df[rpt_cols]
    result = result.sort(['rseq'], ascending=[1])
    return result


def get_records_by_acct_status(status, project_id):
    query = {'acct_status': status}
    if project_id:
        query.update({'project_id': project_id})
    
    captures = db.Capture.query(paginate=False, **query)
    df = pd.DataFrame(list(captures))
    
    result = df.sort(['project_id', 'rseq'], ascending=[1, 1])
    result = result[rpt_cols]
    return result


def run(args, target_dir):
    records, report_title = None, None
    print('Generating report...')
    if args.upriser:
        name_fmt = 'captures-by-upriser-%s.xls'
        report_title = name_fmt % args.upriser.replace('/','_')
        records = get_records_by_upriser(args.upriser)
    elif args.acct_status:
        if not args.project_id:
            raise Exception("Project Id/Code required.")
        
        name_fmt = 'captures-by-acct-status-%s-%s.xls'
        report_title = name_fmt % (args.project_id, datetime.today().strftime('%Y%m%d'))
        records = get_records_by_acct_status(args.acct_status, args.project_id)


    # write out file
    if records.index.size > 0:
        filename = os.path.join(target_dir, report_title)
        writer = pd.ExcelWriter(filename)

        records.to_excel(writer)
        writer.save()
        print('success: report written')



if __name__ == '__main__':
    # define parser
    parser = argparse.ArgumentParser(description="Report Generation Script")
    add = parser.add_argument
    add('-u', '--upriser', help="Upriser code")
    add('-p', '--project-id', help="Project code")
    add('-a', '--acct-status', help="Account status")

    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
    
    args = parser.parse_args()            
    run(args, REPORT_DIR)

