"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module contains the resource definitions for retrieving, updating, deleting 
and uploading Fitness Activity and Health Measurements information.

"""

import re
from datetime import date, datetime
from settings import USER_RESOURCE, MONTH2NUM, NUM2MONTH
from session import get_session 


__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.2.2"
__email__ = "aouyar at gmail.com"
__status__ = "Development"

    
class ContentType:
    """Content Types used by Health Graph API"""
    
    USER = 'User'
    PROFILE = 'Profile'
    SETTINGS = 'Settings'
    FITNESS_ACTIVITY = 'FitnessActivity'
    FITNESS_ACTIVITY_FEED = 'FitnessActivityFeed'
    FITNESS_ACTIVITY_SUMMARY = 'FitnessActivitySummary'
    FITNESS_ACTIVITY_NEW = 'NewFitnessActivity'
    FITNESS_ACTIVITY_LIVE = 'LiveFitnessActivity'
    FITNESS_ACTIVITY_LIVE_UPDATE = 'LiveFitnessActivityUpdate'
    FITNESS_ACTIVITY_LIVE_END = 'LiveFitnessActivityCompletion'
    STRENGTH_ACTIVITY = ' StrengthTrainingActivity'
    STRENGTH_ACTIVITY_FEED = 'StrengthTrainingActivityFeed'
    STRENGTH_ACTIVITY_NEW = 'NewStrengthTrainingActivity'
    BACKGROUND_ACTIVITY = 'BackgroundActivitySet'
    BACKGROUND_ACTIVITY_FEED = 'BackgroundActivitySetFeed'
    BACKGROUND_ACTIVITY_NEW = 'NewBackgroundActivitySet'
    SLEEP_MEASUREMENT = 'SleepSet'
    SLEEP_MEASUREMENT_FEED = 'SleepSetFeed'
    SLEEP_MEASUREMENT_NEW = 'NewSleepSet'
    NUTRITION_MEASUREMENT = 'NutritionSet'
    NUTRITION_MEASUREMENT_FEED = 'NutritionSetFeed'
    NUTRITION_MEASUREMENT_NEW = 'NewNutritionSet'
    WEIGHT_MEASUREMENT = 'WeightSet'
    WEIGHT_MEASUREMENT_FEED = 'WeightSetFeed'
    WEIGHT_MEASUREMENT_NEW = 'NewWeightSet'
    GENERAL_BODY_MEASUREMENT = 'GeneralMeasurementSet'
    GENERAL_BODY_MEASUREMENT_FEED = 'GeneralMeasurementSetFeed'
    GENERAL_BODY_MEASUREMENT_NEW = 'NewGeneralMeasurementSet'
    DIABETES_MEASUREMENT = 'DiabetesMeasurementSet'
    DIABETES_MEASUREMENT_FEED = 'DiabetesMeasurementSetFeed'
    DIABETES_MEASUREMENT_NEW = 'NewDiabetesMeasurementSet'
    PERSONAL_RECORDS = 'Records'
    FRIEND = 'Member'
    FRIEND_FEED = 'TeamFeed'
    FRIEND_INVITE = 'Invitation'
    FRIEND_REPLY = 'Reply'
    

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
        

class BaseResource(object):
    
    _content_type = None
    
    def __init__(self, resource = None, session=None):
        if session is not None:
            self._session = session
        else:
            self._session = get_session()
            if self._session is None:
                raise Exception("Error: No active RunKeeper Session.")
        self._resource = resource
        self._data = None
        self.init()
        
    def init(self):
        if self._resource is not None:
            resp = self._session.get(self._resource, self._content_type)
            self._data = resp.json()
        
    @property
    def resource(self):
        return self._resource
    
    @property
    def content_type(self):
        return self._content_type


class BasicResource(BaseResource):
    
    _prop_dict = {}
    _link_dict = {}
    _feed_dict = {}
    
    def __init__(self, resource = None, session=None):
        super(BasicResource, self).__init__(resource, session)
        
    def init(self):
        if self._resource is not None:
            resp = self._session.get(self._resource, self._content_type)
            self._data = resp.json() # TODO - Error Checking
            
    def __len__(self):
        return len(self._prop_dict)
            
    def __getitem__(self, k):
        prop = self._prop_dict.get(k)
        if prop is not None:
            if isinstance(prop, PropSimple):
                return prop.parse(self._data.get(k))
            else:
                return None
        else:
            raise KeyError(k)
        
    def __contains__(self, k):
        return self._prop_dict.has_key(k)
    
    def __iter__(self):
        return self.iterkeys()
    
    def keys(self):
        return self._prop_dict.keys()
    
    def iterkeys(self):
        return self._prop_dict.iterkeys()
            
    def _get_link(self, k):
        prop = self._link_dict.get(k)
        if prop is not None:
            if isinstance(prop, PropLink):
                resource = self._data.get(k)
                cls = globals().get(prop.resource_class)
                if issubclass(cls, BasicResource):
                    return cls(resource, self._session)
                else:
                    pass
            else:
                pass
        else:
            raise KeyError(k)
        
    def _get_iter(self, k):
        prop = self._feed_dict.get(k)
        if prop is not None:
            if isinstance(prop, PropFeed):
                resource = self._data.get(k)
                cls = globals().get(prop.resource_class)
                if issubclass(cls, ResourceIter):
                    return cls(resource, self._session)
                else:
                    pass
            else:
                pass
        else:
            raise KeyError(k)


class ResourceListItem(BasicResource):
    
    def __init__(self, resource, data, session = None):
        super(BasicResource, self).__init__(resource, session)
        self._data = data
        
    def init(self):
        pass

       
class ResourceIter(BaseResource):
    
    _list_item_class = None
    
    def __init__(self, resource, session=None):
        super(ResourceIter, self).__init__(resource, session)
        
    def __iter__(self):
        if self._list_item_class is None:
            pass
        if self._data is not None:
            while True:
                for itm in self._data['items']:
                    yield self._list_item_class(self._resource, itm, self._session)
                if not self._next_page():
                    raise StopIteration
        else:
            pass
       
    def _next_page(self):
        if self._data is not None:
            next_page = self._data.get('next')
            if next_page is not None:
                self._resource = next_page
                self.init()
                return True
        else:
            return False
    
    @property
    def size(self):
        if self._data is not None:
            return self._data.get('size', 0)
        else:
            pass
         

class User(BasicResource):
    
    _content_type = ContentType.USER
    _prop_dict = {'userID': PropString(),
                  }
    _link_dict = {'profile': PropLink('Profile'),
                  'settings': PropLink('Settings')
                  }
    
    _feed_dict = {'fitness_activities': PropFeed('FitnessActivityIter'),}
    
    def __init__(self, session=None):
        super(User, self).__init__(USER_RESOURCE, session)
        
    def get_profile(self):
        return self._get_link('profile')
    
    def get_settings(self):
        return self._get_link('settings')
    
    def iter_fitness_activities(self):
        return self._get_iter('fitness_activities')
    

class Profile(BasicResource):
    
    _content_type = ContentType.PROFILE
    _prop_dict = {'name': PropString(),
                  'location': PropString(),
                  'athlete_type': PropString(editable=True),
                  'gender': PropString(),
                  'birthday': PropDate(),
                  'elite': PropBoolean(),
                  'profile': PropString(),
                  'small_picture': PropString(),
                  'normal_picture': PropString(),
                  'medium_picture': PropString(),
                  'large_picture': PropString(),
                  }
    
    def __init__(self, resource, session=None):
        super(Profile, self).__init__(resource, session)


class Settings(BasicResource):
    
    _content_type = ContentType.SETTINGS
    _prop_dict = {'facebook_connected': PropBoolean(),
                  'twitter_connected': PropBoolean(),
                  'foursquare_connected': PropBoolean(),
                  'share_fitness_activities': PropString(editable=True),
                  'share_map': PropString(editable=True),
                  }
    
    def __init__(self, resource, session=None):
        super(Settings, self).__init__(resource, session)
        
        
class FitnessActivityListItem(ResourceListItem):
    
    _prop_dict = {'duration': PropInteger(),
                  'start_time': PropDateTime(),
                  'type': PropString(),}
    _link_dict = {}
    
    def __init__(self, resource, data, session = None):
        super(FitnessActivityListItem, self).__init__(resource, data, session)
        

class FitnessActivityIter(ResourceIter):
    
    _contentType = ContentType.FITNESS_ACTIVITY_FEED
    _list_item_class = FitnessActivityListItem
    
    def __init__(self, resource, session=None):
        super(FitnessActivityIter, self).__init__(resource, session)
        

        