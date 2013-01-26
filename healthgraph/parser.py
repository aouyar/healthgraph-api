"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module contains the classes and methods for parsing Health Graph API data.

"""

import re
from datetime import date, datetime
from settings import MONTH2NUM, NUM2MONTH

__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.3.0"
__email__ = "aouyar at gmail.com"
__status__ = "Development"

    
def parse_bool(val):
    if isinstance(val, bool):
        return val
    elif val.lower() == 'true':
        return True
    elif val.lower() == 'false':
        return False
    else:
        return None

def parse_date(val,):
    mobj = re.match('\w+,\s*(\d+)\s+(\w+)\s+(\d+)', val)
    if mobj is not None:
        return date(int(mobj.group(3)), 
                    MONTH2NUM[mobj.group(2)],
                    int(mobj.group(1)))
            
def parse_datetime(val):
    mobj = re.match('\w+,\s*(\d+)\s+(\w+)\s+(\d+)\s+(\d+):(\d+):(\d+)', val)
    if mobj is not None:
        return datetime(int(mobj.group(3)), 
                        MONTH2NUM[mobj.group(2)],
                        int(mobj.group(1)),
                        int(mobj.group(4)),
                        int(mobj.group(5)),
                        int(mobj.group(6)),)
        
def parse_distance(val):
    try:
        return float(val) / 1000
    except:
        return None
    
def parse_distance_km(val):
    try:
        return float(val)
    except:
        return None
    
def parse_resource_dict(prop_defs, data):
    prop_dict = dict([(k, None) for k in prop_defs])
    for k,v in data.items():
        if prop_defs.has_key(k):
            action = prop_defs[k]
            if action is None:
                prop_dict[k] = v
            elif callable(action):
                prop_dict[k] = action(v)
        else:
            pass
    return prop_dict

