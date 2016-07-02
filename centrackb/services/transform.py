"""
Transform json data from on form to another.
"""
from datetime import datetime
from dateutil.parser import parse

RULES = {
    'instance': {
        'excludes': [
            '_bamboo_dataset_id',
            'meta/instanceID',
            '_geolocation',
        ],
        'name_map': {
            'multi_source': 'multi',
            'occupant_status': 'occupant',
            'neighbour_rseqid': 'neighbour_rseq',
            'cust_gps_coord': 'gps',
            'addr_gps': 'gps',
            'rseqId': 'rseq',
            
            # form-08 compatible
            'addy_landmark': 'addr_landmark',
            'addy_house_no': 'addr_no',
            'addy_street': 'addr_street',
            'addy_town_city': 'addr_town',
            'addy_state': 'addr_state',
            'addy_lga': 'addr_lga',
            
            'new_tholder': 'landlord_name',
            'tariff_new': 'tariff_pp',
            'kg_Id': 'kangis_no',
        },
        'name_map2': {  
            ## form-08 entries
            ## -- no longer required -- now defacto as
            ## form-07 & less would be adjusted to match this
            
            #'kangis_no': 'kg_Id',
            #'addr_no':'addy_no',
            #'addr_street':'addy_street',
            #'addr_state':'addy_state',
            #'addr_lga':'addy_lga',
            #'tariff_pp': 'tariff_new',
            #'landlord_name':'new_tholder',
        },
        'transform': [
            'cin_station',
            'cust_name',
            'enum_id',
            'rseq',
        ],
    }
}

def _norm_dates(entry):
    date_fields = ['_submission_time', 'datetime_start', 'datetime_end',
        'datetime_today']
    for f in date_fields:
        entry[f] = parse(entry[f])


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
    rseq = target['rseq']
    target['group'] = target['enum_id'][0]
    target['station'] = rseq[:6]
    target['upriser'] = rseq[:8]
    target['date_created'] = today_date
    target['last_updated'] = None
    target['validated'] = False
    target['snapshots'] = {}
    target['dropped'] = False
    
    ## centrak compatibility
    target['cin_station'] = target['station']
    target['cin_ltroute'] = "{}/00/00".format(rseq[7])
    target['cin_custno'] = rseq[-4:]
    target['cin'] = "{}/{}/{}".format(
        target['cin_station'], 
        target['cin_ltroute'],
        target['cin_custno'])
    
    if 'neighbour_rseq' in target and target['neighbour_rseq']:
        target['neighbour_cin'] = target['neighbour_rseq'][-4:]
    
    _norm_dates(target)
    return target


def ndc_flatten_dict(entry):
    """Transforms Onadata form instance json to consumable form."""
    target = {}
    today_date = datetime.now()
    rules_excl  = RULES['instance']['excludes']
    rules_nmap  = RULES['instance']['name_map']
    rules_nmap2 = RULES['instance']['name_map2']
    rules_xfrm  = RULES['instance']['transform']

    for key,value in entry.items():
        if key in rules_excl:
            continue
        
        last_key = None
        if '/' in key:
            # exclude entries
            key_lpart, key_rpart = key.split('/')
            if key_rpart in rules_excl:
                continue
            
            # re-map names
            if key_rpart in rules_nmap:
                key_rpart = rules_nmap[key_rpart]
            
            # re-map for nerc
            elif key_rpart in rules_nmap2:
                target[key_rpart] = value
                key_rpart = rules_nmap2[key_rpart]
            
            target[key_rpart] = value
            last_key = key_rpart
        else:
            last_key = key
            target[key] = value
        
        # text transform
        if last_key in rules_xfrm:
            target[last_key] = target[last_key].upper()
        last_key = None
    
    # other transforms
    # -------------------------------------------------------------------
    if 'gps' in target:
        target['gps'] = [float(v) for v in target['gps'].split(' ')]
    else:
        target['gps'] = []

    _xform_id_str = target['_xform_id_string'].replace('_nerc', '')
    parts = _xform_id_str.split('_')
    xform_id = "{}_{}_{}".format(parts[0], parts[1][:2], parts[2])
    target['project_id'] = xform_id
    
    target['group'] = target['enum_id'][0]
    target['station'] = target['cin_station']
    target['upriser'] = "{}/{}".format(target['cin_station'], target['cin_ltroute'][0])
    target['cin'] = "{}/{}/{}".format(target['cin_station'], target['cin_ltroute'], target['cin_custno'])
    target['rseq'] = "{}/{}".format(target['upriser'], target['cin_custno'])
    target['date_created'] = today_date
    target['last_updated'] = None
    target['validated'] = False
    target['snapshots'] = {}
    target['dropped'] = False

    if 'neighbour_cin' in target and target['neighbour_cin']:
        target['neighbour_rseq'] = "{}/{}".format(target['upriser'], target['neighbour_cin'])
    
    _norm_dates(target)
    return target

