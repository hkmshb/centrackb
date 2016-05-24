"""
Application wide settings.
"""
import os
import sys
from secret import *



# directory paths
BASE_DIR = os.path.dirname(__file__)


# check that key settings are provided in secret.py module
try:
    DUMP_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', DUMP_DIR_NAME))
    API_DEFAULT_TOKEN = API_TOKEN_EAGLE_EYE
except NameError:
    msg = ('secret.py is expected to define some key application configurations '
           'refer to documentation to see list of expected configurations.')
    print(msg)
    sys.exit(0)

# other dirs
REPORTS_DIR = os.path.join(DUMP_DIR, '_reports')


# API
AUTH_HEADER = {
    'Authorization': 'Token ' + API_DEFAULT_TOKEN 
}

MONGODB_NAME = 'centrak'


# pagination
PAGE_SIZE = 50
NL_PAGE_SIZE = 100
XL_PAGE_SIZE = 200

# formats
FMT_SHORTDATE = '%Y-%m-%d'

# reportings
report_cols = [
    # gen
    'datetime_today', 'station', 'rseq', 'enum_id', 
    # cust-info
    'cust_name', 'cust_mobile1', 'addy_no', 'addy_street', 
    # acct-info
    'acct_status', 'book_code', 'acct_no', 'tariff', 
    'tariff_new',
    # meter-status
    'meter_status', 'meter_no', 'meter_type', 'amt_4_adc',
    # others
    'plot_type', 'occupant', 'gps', 'remarks'
]
