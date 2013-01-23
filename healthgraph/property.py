"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module contains the definitions for the Property Type classes used by
the resource classes.

"""

import re
from datetime import date, datetime
from settings import MONTH2NUM, NUM2MONTH

__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.2.2"
__email__ = "aouyar at gmail.com"
__status__ = "Development"


class Prop:

    pass
    

class PropSimple(Prop):

    parse = None
    
    def __init__(self, editable=False):
        self.editable = False
        
    def parse(self, val):
        return val
    

class PropString(PropSimple):
    
    pass


class PropInteger(PropSimple):
    
    pass


class PropBoolean(PropSimple):
    
    def parse(self, val):
        if val == 'true':
            return True
        elif val == 'false':
            return False
        else:
            return None

        
class PropDate(PropSimple):
    
    def parse(self, val):
        mobj = re.match('\w+,\s*(\d+)\s+(\w+)\s+(\d+)', val)
        if mobj is not None:
            return date(int(mobj.group(3)), 
                        MONTH2NUM[mobj.group(2)],
                        int(mobj.group(1)))

            
class PropDateTime(PropSimple):
    
    def parse(self, val):
        mobj = re.match('\w+,\s*(\d+)\s+(\w+)\s+(\d+)\s+(\d+):(\d+):(\d+)', val)
        if mobj is not None:
            return datetime(int(mobj.group(3)), 
                            MONTH2NUM[mobj.group(2)],
                            int(mobj.group(1)),
                            int(mobj.group(4)),
                            int(mobj.group(5)),
                            int(mobj.group(6)),)

class PropLink(Prop):

    def __init__(self, resource_class):
        
        self.resource_class = resource_class
        

class PropFeed(Prop):
    
    def __init__(self, resource_class):
        
        self.resource_class = resource_class
