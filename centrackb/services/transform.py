"""
Transform json data from on form to another.                             
"""
from datetime import datetime


RULES = {
    'instance': {
        'excludes': [
            '_bamboo_dataset_id',
            'meta/instanceID',
            '_geolocation',
        ],
        'name_map': {
            'addy_house_no': 'addy_no',
            'multi_source': 'multi',
            'occupant_status': 'occupant',
            'neighbour_rseqid': 'neighbour_rseq',
            'cust_gps_coord': 'gps',
            'rseqId': 'rseq',
        },
        'transform': [
            'cust_name',
            'enum_id',
            'rseq',
        ],
    }
}


def to_nested_dict(d):
    """Unflatten the dictionary keys used in the provided dictionary"""
    target = {}
    rules_excl = RULES['instance']['excludes']
    rules_nmap = RULES['instance']['name_map']

    for k, v in d.items():
        if k in rules_excl:
            continue

        if '/' in k:
            # flatten key
            key, ikey = k.split('/')
            if key.endswith('_info'):
                key = key.replace('_info','')
            
            if ikey in rules_nmap:
                ikey = rules_nmap[ikey]
            
            if '_' in ikey:
                ikey = '_'.join(ikey.split('_')[1:])

            # set keys
            if key not in target:
                target[key] = {}
            target[key][ikey] = v
        else:
            target[k] = v
    
    # direct transform
    #--------------------------------------------------------
    gps = target['address']['gps_coord']
    target['gps_coord'] = [float(v) for v in gps.split(' ')]
    del target['address']['gps_coord']
    
    target['rseq'] = target['source']['rseqId']
    del target['source']['rseqId']
    if 'kg_id' in target['source']:
        target['kangis_id'] = target['source']['kg_id']
    del target['source']

    target['title_holder'] = target['address']['tholder']
    del target['address']['tholder']

    target['enum_id'] = target['enum']['id']
    del target['enum']

    target['meter']['status'] = target['meter_status']
    del target['meter_status']

    # return processed dict
    return target


def to_flatten_dict(entry):
    """Remove group names from key-name"""
    target = {}
    today_date = datetime.today().date().isoformat()
    rules_excl = RULES['instance']['excludes']
    rules_nmap = RULES['instance']['name_map']
    rules_xfrm = RULES['instance']['transform']

    for k, v in entry.items():
        if k in rules_excl:
            continue

        last_key = None
        if '/'  in k:
            # exclude entries
            key, ikey = k.split('/')
            if ikey in rules_excl:
                continue

            # re-map names
            if ikey in rules_nmap:
                ikey = rules_nmap[ikey]
            
            last_key = ikey
            target[ikey] = v
        else:
            last_key = k
            target[k] = v
        
        # text transform
        if last_key in rules_xfrm:
            target[last_key] = target[last_key].upper()
        last_key = None

    # other transforms
    #----------------------------------------------------------
    if 'gps' in target:
        target['gps'] = [float(v) for v in target['gps'].split(' ')]
    else:
        target['gps'] = []
    
    # add new entries
    ## set project_id
    # HACK: treats Hotoro 11KV feeder entries with special care
    _xform_id_str = target['_xform_id_string']
    if _xform_id_str.startswith('cust'):
        if _xform_id_str.startswith('custform0'):
            target['project_id'] = 'f13e_cf_KN'
        else:
            target['project_id'] = 'f13e_cu_KN'
        
        target['enum_id'] = 'X/4Q2015'
    else:
        parts = _xform_id_str.split('_')
        xform_id = '%s_%s_%s' % (parts[0], parts[1][:2],  parts[2])
        target['project_id'] = xform_id
    
    ## more entries
    target['group'] = target['enum_id'][0]
    target['station'] = target['rseq'][:6]
    target['upriser'] = target['rseq'][:8]
    target['date_created'] = today_date
    target['last_updated'] = None
    target['validated'] = False
    target['snapshots'] = {}
    target['dropped'] = False
    return target

