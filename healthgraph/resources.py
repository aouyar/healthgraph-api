"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module contains the resource definitions for retrieving, updating, deleting 
and uploading Fitness Activity and Health Measurements information.

"""

import urllib
import urlparse
import inspect
from collections import namedtuple, MutableMapping
import settings
import content_type
import sessionmgr
from parser import (parse_resource_dict, 
                    parse_bool, 
                    parse_distance, parse_distance_km, 
                    parse_date, parse_datetime, 
                    parse_date_param)


__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.3.0"
__email__ = "aouyar at gmail.com"
__status__ = "Development"

    
class PersonalRecordType:
    """Personal record types."""    
    
    THIS_WEEK = 'THIS_WEEK'
    THIS_MONTH = 'THIS_MONTH'
    LAST_WEEK = 'LAST_WEEK'
    LAST_MONTH = 'LAST_MONTH'
    OVERALL = 'OVERALL'
    BEST_ACTIVITY = 'BEST_ACTIVITY'
    BEST_WEEK = 'BEST_WEEK'
    BEST_MONTH = 'BEST_MONTH'


class ResourceLink(namedtuple('ResourceLink', ('clsname', 'resource'))):
    pass


class PropResourceLink(object):
    
    def __init__(self, clsname):
        self._clsname = clsname
    
    def __call__(self, resource=None):
        return ResourceLink(self._clsname, resource)
    

class ContainerMixin(MutableMapping):
    
    def __getitem__(self, k):
        return self._prop_dict[k]
    
    def __setitem__(self, k, v):
        self._prop_dict[k] = v
        
    def __delitem__(self, k):
        del self._prop_dict[k]
        
    def __len__(self):
        return len(self._prop_dict)
    
    def __iter__(self):
        return iter(self._prop_dict)


class APIobject(object):
    _prop_defs = None
    _prop_main = None
    
    def __init__(self, session=None):
        self._prop_dict = {}
        self._resource = None
        if session is not None:
            self._session = session
        else:
            self._session = sessionmgr.get_session()
            
    def _get_resource_data(self, resource, content_type, params=None):
        resp = self._session.get(resource, content_type, params)
        return resp.json() # TODO - Error Checking
    
    def _get_linked_resource(self, link, cls_override=None, **kwargs):
        if link is not None:
            if cls_override is None:
                cls = globals().get(link.clsname)
            else:
                cls = globals().get(cls_override)
            if inspect.isclass(cls) and issubclass(cls, BaseResource):
                return cls(link.resource, session=self._session, **kwargs)
            else:
                pass
        else:
            return None
        
    def __str__(self):
        if self._resource is not None:
            prop_strs = ["resource=%s" % self._resource,]
        else:
            prop_strs = []
        for k in self._prop_main:
            if self._prop_dict[k] is not None:
                prop_strs.append("%s=%s" % (k, self._prop_dict[k]))
        return "HealthGraph API: %s(%s)" % (self.__class__.__name__,
                                             ', '.join(prop_strs))


class BaseResource(APIobject):
    
    _content_type = None
    
    def __init__(self, resource = None, session=None, params=None):
        super(BaseResource,self).__init__(session=session)
        self._resource = resource
        self.load(params)
            
    @property
    def resource(self):
        return self._resource
    
    @property
    def content_type(self):
        return self._content_type
    
    def load(self, params=None):
        if self._resource is not None:
            data = self._get_resource_data(self._resource, self._content_type, 
                                            params)
            self._prop_dict = self._parse_data(data)
            
    def _parse_data(self, data):
        return parse_resource_dict(self._prop_defs, data)


class ResourceItem(APIobject, ContainerMixin):

    def __init__(self, data=None, session=None):
        super(ResourceItem, self).__init__(session=session)
        if data is not None:
            self._prop_dict = parse_resource_dict(self._prop_defs, data)
        else:
            self._prop_dict = {}

        
class Resource(BaseResource, ContainerMixin):
    
    def __init__(self, resource = None, params=None, session=None):
        super(Resource, self).__init__(resource, params=params, session=session)


class ResourceFeedIter(BaseResource):
    
    _prop_defs = {'size': None,
                  'items': None,
                  'previous': PropResourceLink('ResourceFeedIter'),
                  'next': PropResourceLink('ResourceFeedIter')}
    _item_cls = None
    _prop_main = ('size',)
    
    def __init__(self, resource, 
                 date_min=None, date_max=None, 
                 mod_date_min=None, mod_date_max=None,
                 descending=True,
                 session=None):
        func_params = locals()
        params = {'pageSize': settings.DEFAULT_PAGE_SIZE,}
        for func_key, api_key in (('date_min', 'noEarlierThan'),
                                  ('date_max', 'noLaterThan'),
                                  ('mod_date_min', 'modifiedNoEarlierThan'),
                                  ('mod_date_max', 'modifiedNoLater'),):
            val = parse_date_param(func_params[func_key])
            if val is not None:
                params[api_key] = val
        super(ResourceFeedIter, self).__init__(resource, params=params,
                                               session=session)
        self._descending = descending
        if descending:
            self._iter = iter(self._prop_dict['items'])
        else:
            self._last_page()
            self._iter = reversed(self._prop_dict['items'])
            
        
    def count(self):
        return self._prop_dict['size']
             
    def __iter__(self):
        if self._item_cls is not None:
            return self
        else:
            pass
    
    def next(self):
        try:
            item = self._iter.next()
        except StopIteration:
            if self._descending and self._next_page():
                self._iter = iter(self._prop_dict['items'])
                item = self._iter.next()
            elif not self._descending and self._prev_page():
                self._iter = reversed(self._prop_dict['items'])
                item = self._iter.next()
            else:
                raise StopIteration
        return self._item_cls(item, self._session)
                
    def _prev_page(self):
        link = self._prop_dict.get('previous')
        if link is not None:
            self._resource = link.resource
            self.load()
            return True
        else:
            return False
    
    def _next_page(self):
        link = self._prop_dict.get('next')
        if link is not None:
            self._resource = link.resource
            self.load()
            return True
        else:
            return False
        
    def _last_page(self):
        link = self._prop_dict.get('next')
        if link is not None:
            size = self.count()
            last_page = size / settings.DEFAULT_PAGE_SIZE
            if size % settings.DEFAULT_PAGE_SIZE == 0:
                last_page -= 1
            if last_page > 0:
                self._resource, qs = urllib.splitquery(link.resource)
                params = urlparse.parse_qs(qs)
                params['page'] = last_page
                self.load(params=params)
                return True
            else:
                return False
        else:
            return False


class FeedItem(ResourceItem):
    
    def __init__(self, data, session=None):
        super(FeedItem, self).__init__(data, session=session)


class User(Resource):
    
    _content_type = content_type.USER
    _prop_defs = {'userID': None,
                  'profile': PropResourceLink('Profile'),
                  'settings': PropResourceLink('Settings'),
                  'fitness_activities': PropResourceLink('FitnessActivityIter'),
                  'strength_training_activities': PropResourceLink('StrengthActivityIter'),
                  'background_activities': PropResourceLink('BackgroundActivityIter'),
                  'sleep': PropResourceLink('SleepMeasurementIter'),
                  'nutrition': PropResourceLink('NutritionMeasurementIter'),
                  'weight': PropResourceLink('WeightMeasurementIter'),
                  'general_measurements': PropResourceLink('GeneralMeasurementIter'),
                  'diabetes': PropResourceLink('DiabetesMeasurementIter'),
                  'records': PropResourceLink('PersonalRecords'),
                  'team': PropResourceLink('FriendIter'),                
                  }
    _prop_main = ('userID',)
    
    def __init__(self, session=None):
        super(User, self).__init__(settings.USER_RESOURCE, session=session)
    
    def get_profile(self):
        return self._get_linked_resource(self._prop_dict['profile'])
        
    def get_settings(self):
        return self._get_linked_resource(self._prop_dict['settings'])
    
    def get_records(self):
        return self._get_linked_resource(self._prop_dict['records'])
    
    def get_fitness_activity_iter(self, 
                                  date_min=None, date_max=None, 
                                  mod_date_min=None, mod_date_max=None,
                                  descending=True):
        return self._get_linked_resource(self._prop_dict['fitness_activities'],
                                         date_min=date_min, 
                                         date_max=date_max,
                                         mod_date_min=mod_date_min,
                                         mod_date_max=mod_date_max,
                                         descending=descending)
    
    def get_strength_activity_iter(self,
                                   date_min=None, date_max=None, 
                                   mod_date_min=None, mod_date_max=None,
                                   descending=True):
        return self._get_linked_resource(self._prop_dict['strength_training_activities'],
                                         date_min=date_min, 
                                         date_max=date_max,
                                         mod_date_min=mod_date_min,
                                         mod_date_max=mod_date_max,
                                         descending=descending)
    
    def get_weight_measurement_iter(self,
                                    date_min=None, date_max=None, 
                                    mod_date_min=None, mod_date_max=None,
                                    descending=True):
        return self._get_linked_resource(self._prop_dict['weight'],
                                         date_min=date_min, 
                                         date_max=date_max,
                                         mod_date_min=mod_date_min,
                                         mod_date_max=mod_date_max,
                                         descending=descending)
    

class Profile(Resource):
    
    _content_type = content_type.PROFILE
    _prop_defs = {'name': None,
                  'location': None,
                  'athlete_type': None,
                  'gender': None,
                  'birthday': parse_date,
                  'elite': parse_bool,
                  'profile': None,
                  'small_picture': None,
                  'normal_picture': None,
                  'medium_picture': None,
                  'large_picture': None,
                  }
    _prop_main = ('name', 'gender', 'birthday',)
    
    def __init__(self, resource, session=None):
        super(Profile, self).__init__(resource, session=session)


class Settings(Resource):
    
    _content_type = content_type.SETTINGS
    _prop_defs = {'facebook_connected': parse_bool,
                  'twitter_connected': parse_bool,
                  'foursquare_connected': parse_bool,
                  'share_fitness_activities': None,
                  'share_map': None,
                  'post_fitness_activity_facebook': parse_bool,
                  'post_fitness_activity_twitter': parse_bool,
                  'post_live_fitness_activity_facebook': parse_bool,
                  'post_live_fitness_activity_twitter': parse_bool,
                  'share_background_activities': None,
                  'post_background_activity_facebook': parse_bool,
                  'post_background_activity_twitter': parse_bool,
                  'share_sleep': None,
                  'post_sleep_facebook': parse_bool,
                  'post_sleep_twitter': parse_bool,
                  'share_nutrition': None,
                  'post_nutrition_facebook': parse_bool,
                  'post_nutrition_twitter': parse_bool,
                  'share_weight': None,
                  'post_weight_facebook': parse_bool,
                  'post_weight_twitter': parse_bool,
                  'share_general_measurements': None,
                  'post_general_measurements_facebook': parse_bool,
                  'post_general_measurements_twitter': parse_bool,
                  'share_diabetes': None,
                  'post_diabetes_facebook': parse_bool,
                  'post_diabetes_twitter': parse_bool,
                  'distance_units': None,
                  'weight_units': None,
                  'first_day_of_week': None,
                  }
    
    def __init__(self, resource, session=None):
        super(Settings, self).__init__(resource, session=session)
      

class PersonalRecords(Resource):
    
    _content_type = content_type.PERSONAL_RECORDS

    def __init__(self, resource, session=None):
        super(PersonalRecords, self).__init__(resource, session=session)

    def _parse_data(self, data):
        prop_dict = {'totals': {}, 'bests': {},}
        for actrecs in data:
            totals = {}
            bests = {}
            overall = 0
            act_type = actrecs['activity_type']
            for stats in actrecs['stats']:
                stat_type = stats['stat_type']
                stat_date = stats.get('date')
                if stat_type == 'OVERALL':
                    stat_dist = parse_distance(stats['value'])
                    overall = stat_dist
                else:
                    stat_dist = parse_distance_km(stats['value'])
                if stat_date is None:
                    totals[stat_type] = stat_dist
                else:
                    bests[stat_type] = (stat_date, stat_dist)
            if overall > 0:
                if len(totals) > 0:
                    prop_dict['totals'][act_type] = totals
                if len(bests) > 0:
                    prop_dict['bests'][act_type] = bests
        return prop_dict
    
    def get_activity_types(self):
        return self._prop_dict.keys()
    
    def get_totals(self):
        return self._prop_dict['totals']
    
    def get_bests(self):
        return self._prop_dict['bests']
    
    def get_activity_totals(self, activity_type):
        try:
            return self._prop_dict['totals'][activity_type]
        except KeyError:
            return None
    
    def get_activity_bests(self, activity_type):
        try:
            return self._prop_dict['bests'][activity_type]
        except KeyError:
            return None


class FitnessActivity(Resource):
    
    _content_type = content_type.FITNESS_ACTIVITY
    _prop_defs = {'uri': PropResourceLink('FitnessActivity'),
                  'userID': None,
                  'type': None,
                  'secondary_type': None,
                  'equipment': None,
                  'start_time': parse_datetime,
                  'total_distance': parse_distance,
                  'distance': None,
                  'duration': None,
                  'average_heart_rate': None,
                  'heart_rate': None,
                  'total_calories': None,
                  'calories': None,
                  'climb': None,
                  'notes': None,
                  'is_live': parse_bool,
                  'path': None,
                  'images': None,
                  'source': None,
                  'activity': None,
                  'comments': None,
                  'previous': PropResourceLink('FitnessActivity'),
                  'next': PropResourceLink('FitnessActivity'),
                  'nearest_teammate_fitness_activities': None,
                  'nearest_strength_training_activity': None,
                  'nearest_teammate_strength_training_activities': None,
                  'nearest_background_activity': None,
                  'nearest_teammate_background_activities': None,
                  'nearest_sleep': None,
                  'nearest_teammate_sleep': None,
                  'nearest_nutrition': None,
                  'nearest_teammate_nutrition': None,
                  'nearest_weight': None,
                  'nearest_teammate_weight': None,
                  'nearest_general_measurement': None,
                  'nearest_teammate_general_measurements': None,
                  'nearest_diabetes': None,
                  'nearest_teammate_diabetes': None,
                  }
    
    _prop_main = ('type', 'start_time',)
    
    def __init__(self, resource, session=None):
        super(FitnessActivity, self).__init__(resource, session=session)

    def get_prev_activity(self):
        return self._get_linked_resource(self._prop_dict['previous'])
    
    def get_next_activity(self):
        return self._get_linked_resource(self._prop_dict['next'])
    

class FitnessActivitySummary(Resource):
    
    _content_type = content_type.FITNESS_ACTIVITY_SUMMARY
    _prop_defs = {'uri': PropResourceLink('FitnessActivity'),
                  'userID': None,
                  'type': None,
                  'secondary_type': None,
                  'equipment': None,
                  'start_time': parse_datetime,
                  'total_distance': parse_distance,
                  'duration': None,
                  'average_heart_rate': None,
                  'total_calories': None,
                  'climb': None,
                  'notes': None,
                  'is_live': parse_bool,
                  'source': None,
                  'activity': None,
                  }
    _prop_main = ('type', 'start_time',)
    
    def __init__(self, resource, session=None):
        super(FitnessActivitySummary, self).__init__(resource, session=session)
        
    def get_activity_detail(self):
        return self._get_linked_resource(self._prop_dict['uri'])
    

class FitnessActivityFeedItem(FeedItem):
    
    _prop_defs = {'start_time': parse_datetime,
                  'type': None,
                  'duration': None,
                  'total_distance': parse_distance,
                  'uri': PropResourceLink('FitnessActivity'),
                  }
    _prop_main = ('type', 'start_time',)
    
    def __init__(self, data, session=None):
        super(FitnessActivityFeedItem, self).__init__(data, session=session)
        
    def get_activity_detail(self):
        return self._get_linked_resource(self._prop_dict['uri'])
    
    def get_activity_summary(self):
        return self._get_linked_resource(self._prop_dict['uri'], 'FitnessActivitySummary')


class FitnessActivityIter(ResourceFeedIter):
    
    _content_type = content_type.FITNESS_ACTIVITY_FEED
    _item_cls = FitnessActivityFeedItem
    
    def __init__(self, resource, 
                 date_min=None, date_max=None, 
                 mod_date_min=None, mod_date_max=None,
                 descending=True,
                 session=None):
        super(FitnessActivityIter, self).__init__(resource,
                                                  date_min=date_min,
                                                  date_max=date_max,
                                                  mod_date_min=mod_date_min,
                                                  mod_date_max=mod_date_max,
                                                  descending=descending,
                                                  session=session)


class StrengthActivityFeedItem(FeedItem):
    
    _prop_defs = {'start_time': parse_datetime,
                  'uri': PropResourceLink('StrengthActivity')}
    _prop_main = ('start_time',)
    
    def __init__(self, data, session=None):
        super(StrengthActivityFeedItem, self).__init__(data, session=session)


class StrengthActivityIter(ResourceFeedIter):
    
    _content_type = content_type.STRENGTH_ACTIVITY_FEED
    _item_cls = StrengthActivityFeedItem
    
    def __init__(self, resource, 
                 date_min=None, date_max=None, 
                 mod_date_min=None, mod_date_max=None,
                 descending=True,
                 session=None):
        super(StrengthActivityIter, self).__init__(resource, 
                                                   date_min=date_min,
                                                   date_max=date_max,
                                                   mod_date_min=mod_date_min,
                                                   mod_date_max=mod_date_max,
                                                   descending=descending, 
                                                   session=session)


class WeightMeasurementFeedItem(FeedItem):
    
    _prop_defs = {'uri': PropResourceLink('WeightMeasurement'),
                  'timestamp': parse_datetime,
                  'weight': float,
                  'height': None,
                  'free_mass': None,
                  'fat_percent': float,
                  'mass_weight': float,
                  'bmi': float}
    _prop_main = ('timestamp',)
    
    def __init__(self, data, session=None):
        super(WeightMeasurementFeedItem, self).__init__(data, session=session)


class WeightMeasurementIter(ResourceFeedIter):
    
    _content_type = content_type.WEIGHT_MEASUREMENT_FEED
    _item_cls = WeightMeasurementFeedItem
    
    def __init__(self, resource, 
                 date_min=None, date_max=None, 
                 mod_date_min=None, mod_date_max=None,
                 descending=True,
                 session=None):
        super(WeightMeasurementIter, self).__init__(resource, 
                                                    date_min=date_min,
                                                    date_max=date_max,
                                                    mod_date_min=mod_date_min,
                                                    mod_date_max=mod_date_max,
                                                    descending=descending, 
                                                    session=session)
