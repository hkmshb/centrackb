"""
This script runs the application using a development server.
"""
import os
import sys
import logging
import logging.config

import bottle
from beaker.middleware import SessionMiddleware

import settings
from utils import MongoDbSetupMiddleware


# routes contains the HTTP handlers for our server and must be imported.
from routes import *



def setup_logging():
    log_conf = os.path.join(settings.BASE_DIR, '..', 'centrackb.json')
    if os.path.exists(log_conf):
        import json
        
        with open(log_conf, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config['logging'])
    else:
        logging.basicConfig(level=logging.INFO)


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


# startup config
application = wsgi_app()
setup_logging()


argv = sys.argv[1:]
if '--debug' in argv or 'SERVER_DEBUG' in os.environ:
    # Debug mode will enable more verbose output in the console window.
    # It must be set at the beginning of the script.
    bottle.debug(True)


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
        'app': application, 'server': 'wsgiref',
        'host': HOST, 'port': PORT }

    if '--reload' in argv:
        run_args['reloader'] = True

    bottle.run(**run_args)
