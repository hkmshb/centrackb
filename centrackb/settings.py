"""
Application wide settings.
"""
import os
import sys
from secret import *


# directory paths
BASE_DIR = os.path.dirname(__file__)
KEDAT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
sys.path.append(KEDAT_DIR)


# API
API_DEFAULT_TOKEN=API_TOKEN_EAGLE_EYE

AUTH_HEADER = {
    'Authorization': 'Token ' + API_DEFAULT_TOKEN 
}


# pagination
PAGE_SIZE = 50
NL_PAGE_SIZE = 100
XL_PAGE_SIZE = 200

# formats
FMT_SHORTDATE = '%Y-%m-%d'

# reportings
report_cols = [
    # gen
    'datetime_today', 'rseq', 'enum_id', 
    # cust-info
    'cust_name', 'cust_mobile1', 'addy_no', 'addy_street', 
    # acct-info
    'acct_status', 'acct_no', 'tariff',
    # meter-status
    'meter_status', 'meter_no', 'meter_type',
    # others
    'plot_type', 'occupant', 'remarks',
]
