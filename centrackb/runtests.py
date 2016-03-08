import os
import sys
import unittest


CENTRAK_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(os.path.join(CENTRAK_DIR, '..', '..'))

sys.path.append(PROJECT_DIR)
sys.path.append(CENTRAK_DIR)



if __name__ == '__main__':

    if '--make-fixture' in sys.argv:
        from tests import make_fixtures
        make_fixtures()
    else:
        start_dir = os.path.join(CENTRAK_DIR, 'tests')

        loader = unittest.TestLoader()
        runner = unittest.TextTestRunner()
        suites =  loader.discover(start_dir)
        runner.run(suites)
