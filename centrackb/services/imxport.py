import io
import csv
try:
    from cString import StringIO
except:
    from io import StringIO

from kedat.core import Storage as _
import db



def _make_imxsummary(result):
    def func():
        return (
            "Import summary. Passed: %s, Failed: %s" %
            (result.passed, result.failed)
        )
    return func


def feeder_stations(feeder, impfile):
    result = _(summary=None, errors=[], passed=0, failed=0)
    result.summary = _make_imxsummary(result)

    try:
        impfile.file.seek(0)
        f = StringIO(impfile.file.read().decode())
        f.seek(0)

        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)

        reader = csv.DictReader(f, dialect=dialect)
        for row in reader:
            try:
                r = {}
                r['code'] = row['code'].upper()
                r['name'] = row['name'].title()
                r['capacity'] = row['capacity']
                r['public'] = row['type'].upper().strip() == 'P'
                r['type'] = row.get('category', '') or 'D'
                r['source_feeder']  = feeder.code
                r['vratio'] = str(db.Volt.MVOLTL_LVOLT 
                        if feeder.voltage == '11'
                        else db.Volt.MVOLTH_LVOLT)
                db.Station.insert_one(r)
                result.passed += 1
            except Exception as ex:
                result.failed += 1
    except Exception as ex:
        result.errors.append(str(ex))
    return result
