"""
Routes (Controller) packages.
"""
import os
from cork import Cork
from cork.backends import SQLiteBackend

from utils import make_auth_decorator
from settings import DUMP_DIR



__all__ = ['admin', 'account', 'api', 'core']
AUDB_DIR = os.path.join(DUMP_DIR, 'centrak-uam.db')   # user-authn-mgmt


# authnz
try: backend = SQLiteBackend(AUDB_DIR, initialize='True')
except: backend = SQLiteBackend(AUDB_DIR)
    
authnz = Cork(backend=backend)
authorize = make_auth_decorator(
                authnz, role='user',
                fail_unauth_redirect='/login',
                fail_auth_redirect="/restricted")
