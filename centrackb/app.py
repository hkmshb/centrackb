"""
This script runs the application using a development server.
"""
import os
import sys
import bottle
from beaker.middleware import SessionMiddleware

import settings
from utils import MongoDbSetupMiddleware


# routes contains the HTTP handlers for our server and must be imported.
from routes import *


argv = sys.argv[1:]
if '--debug' in argv or 'SERVER_DEBUG' in os.environ:
    # Debug mode will enable more verbose output in the console window.
    # It must be set at the beginning of the script.
    bottle.debug(True)

def wsgi_app():
    """Returns the application to make available through wfastcgi. This is used
    when the site is published to Microsoft Azure."""
    session_options = {
        'session.type': 'file',
        # Issue #4 [local-gogs]: session expiration handling
        'session.timeout': 210,     # 210 sec = 3min.30sec
        'session.data_dir': os.path.join(settings.DUMP_DIR, 'session-data'),
        'session.auto': True
    }
    app = SessionMiddleware(bottle.default_app(), session_options)
    app = MongoDbSetupMiddleware(app)
    return app

if __name__ == '__main__':
    """
    expected command line arguments:
        --debug        To run the app in debug mode
        --reload       active when debug is active; causes changes in code to
                       be reloaded automatically by restarting the server
        --no-auth      By-passes the authentication and authorisation process
                       in use by the application. (meant for use during app
                       development, together with the flags above).
    """
    STATIC_ROOT = os.path.join(settings.BASE_DIR, 'static').replace('\\', '/')
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    @bottle.route('/static/<filepath:path>')
    def server_static(filepath):
        """Handler for static files, used with the development server.
        When running under a production server such as IIS or Apache,
        the server should be configured to serve the static files."""
        return bottle.static_file(filepath, root=STATIC_ROOT)

    # Starts a local test server.
    run_args = {
        'app': wsgi_app(), 'server': 'wsgiref',
        'host': HOST, 'port': PORT }

    if '--reload' in argv:
        run_args['reloader'] = True

    bottle.run(**run_args)
