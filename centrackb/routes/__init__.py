"""
Routes (Controller) packages.
"""
import os
from cork import Cork
from cork.backends import SQLiteBackend
from utils import make_auth_decorator



__all__ = ['admin', 'account', 'api', 'core']
_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_aucf_dir = os.path.join(_base_dir, 'auth_conf')
_audb_dir = os.path.join(_base_dir, 'centrak-uam.db')   # user-authn-mgmt


# authnz
try: backend = SQLiteBackend(_audb_dir, initialize='True')
except: backend = SQLiteBackend(_audb_dir)
    
authnz = Cork(backend=backend)
authorize = make_auth_decorator(
                authnz, role='user',
                fail_unauth_redirect='/login',
                fail_auth_redirect="/restricted")
