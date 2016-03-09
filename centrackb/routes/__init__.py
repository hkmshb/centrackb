"""
Routes (Controller) packages.
"""
import os
from cork import Cork
from cork.backends import MongoDBBackend

from utils import make_auth_decorator
from settings import MONGODB_NAME



__all__ = ['admin', 'account', 'api', 'core']


# authnz
backend = MongoDBBackend(db_name=MONGODB_NAME)
    
authnz = Cork(backend=backend)
authorize = make_auth_decorator(
                authnz, role='user',
                fail_unauth_redirect='/login',
                fail_auth_redirect="/restricted")
