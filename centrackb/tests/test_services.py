import os
import json
import unittest
import pandas as pd

from services import stats

BASE_DIR = os.path.dirname(__file__)
FIXT_DIR = os.path.join(BASE_DIR, 'fixtures')


class StatsFixtures(unittest.TestCase):
    filename = 'captures-20160108.json'

    @classmethod
    def setUpClass(cls):
        filepath = os.path.join(FIXT_DIR, cls.filename)
        captures = json.load(open(filepath, 'r'))
        cls.captures = pd.DataFrame(captures)

    
    def test_duplicates_summary(self):
        result = stats.summarize_duplicates(self.captures)
        self.assertEqual(15, result.rseq_duplicates)
        self.assertEqual(1, result.acct_no_duplicates)

    def test_acct_status_summary(self):
        result = stats.summarize_acct_status(self.captures)
        self.assertEqual(19, result.unknown)
        self.assertEqual(11, result.new)
        self.assertEqual(82, result.active)
        self.assertEqual( 6, result.inactive)
        self.assertEqual( 0, result.not_conn)
        self.assertEqual( 0, result.disconn_bill)
        self.assertEqual( 0, result.disconn_no_bill)
        self.assertEqual( 0, result.n_a)

    def test_meter_type_summary(self):
        result = stats.summarize_meter_type(self.captures)
        self.assertEqual(14, result.none)
        self.assertEqual( 3, result.analogue)
        self.assertEqual(54, result.ppm)


if __name__ == '__main__':
    unittest.main()
