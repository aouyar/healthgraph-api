"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module contains the resource definitions for retrieving, updating, deleting 
and uploading Fitness Activity and Health Measurements information.

"""

import inspect
from collections import namedtuple
from settings import USER_RESOURCE
from session import get_session
from parser import (parse_resource_dict, parse_bool, parse_distance, parse_distance_km, 
                    parse_date, parse_datetime,)


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


class ResourceLink(namedtuple('ResourceLink', ('clsname', 'resource'))):
    pass


class PropResourceLink(object):
    
    def __init__(self, clsname):
        self._clsname = clsname
    
    def __call__(self, resource=None):
        return ResourceLink(self._clsname, resource)


class ContainerMixin(object):
    pass


class APIobject(object):
    _prop_defs = {}
    
    def __init__(self, session=None):
        self._prop_dict = {}
        if session is not None:
            self._session = session
        else:
            self._session = get_session()
            
    def _get_resource_data(self, resource, content_type):
        resp = self._session.get(resource, content_type)
        return resp.json() # TODO - Error Checking
    
    def _get_linked_resource(self, link):
        if link is not None:
            cls = globals().get(link.clsname)
            if inspect.isclass(cls) and issubclass(cls, BaseResource):
                return cls(link.resource, self._session)
            else:
                pass
        else:
            return None


class BaseResource(APIobject):
    
    _content_type = None
    
    def __init__(self, resource = None, session=None):
        super(BaseResource,self).__init__(session)
        self._resource = resource
        self.load()
        
    @property
    def resource(self):
        return self._resource
    
    @property
    def content_type(self):
        return self._content_type
    
    def load(self):
        if self._resource is not None:
            data = self._get_resource_data(self._resource, self._content_type)
            self._prop_dict = self._parse_data(data)
            
    def _parse_data(self, data):
        return parse_resource_dict(self._prop_defs, data)


class ResourceItem(BaseResource, ContainerMixin):

    def __init__(self, data, session=None):
        super(ResourceItem, self).__init__(None, session)
        self._prop_dict = parse_resource_dict(self._prop_defs, data)

        
class Resource(BaseResource, ContainerMixin):
    
    def __init__(self, resource = None, session=None):
        super(Resource, self).__init__(resource, session)


class ResourceFeedIter(BaseResource):
    
    _prop_defs = {'size': None,
                  'items': None,
                  'previous': PropResourceLink('ResourceFeedIter'),
                  'next': PropResourceLink('ResourceFeedIter')}
    _item_cls = None
    
    def __init__(self, resource, session=None):
        super(ResourceFeedIter, self).__init__(resource, session)
        self._iter = iter(self._prop_dict['items'])
             
    def __iter__(self):
        if self._item_cls is not None:
            return self
        else:
            pass
    
    def next(self):
        try:
            item = self._iter.next()
        except StopIteration:
            if self._next_page():
                self._iter = iter(self._prop_dict['items'])
                item = self._iter.next()
            else:
                raise StopIteration
        return self._item_cls(item, self._session)
                
    def _prev_page(self):
        link = self._prop_dict.get('prev')
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


class FeedItem(ResourceItem):
    
    def __init__(self, data, session=None):
        super(FeedItem, self).__init__(data, session)


class User(Resource):
    
    _content_type = ContentType.USER
    _prop_defs = {'userID': None,
                  'profile': PropResourceLink('Profile'),
                  'settings': PropResourceLink('Settings'),
                  'fitness_activities': PropResourceLink('FitnessActivityIter'),
                  'strength_training_activities': PropResourceLink('StrengthActivityIter'),
                  'background_activities': PropResourceLink(''),
                  'sleep': PropResourceLink(''),
                  'nutrition': PropResourceLink(''),
                  'weight': PropResourceLink(''),
                  'general_measurements': PropResourceLink(''),
                  'diabetes': PropResourceLink(''),
                  'records': PropResourceLink('PersonalRecords'),
                  'team': PropResourceLink(''),                
                  }
    
    _feed_dict = {'fitness_activities': 'FitnessActivityIter',}
    
    def __init__(self, session=None):
        super(User, self).__init__(USER_RESOURCE, session)
    
    def get_profile(self):
        return self._get_linked_resource(self._prop_dict['profile'])
        
    def get_settings(self):
        return self._get_linked_resource(self._prop_dict['settings'])
    
    def get_records(self):
        return self._get_linked_resource(self._prop_dict['records'])
    
    def get_fitness_activity_iter(self):
        return self._get_linked_resource(self._prop_dict['fitness_activities'])
    
    def get_strength_activity_iter(self):
        return self._get_linked_resource(self._prop_dict['strength_training_activities'])
    

class Profile(Resource):
    
    _content_type = ContentType.PROFILE
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
    
    def __init__(self, resource, session=None):
        super(Profile, self).__init__(resource, session)


class Settings(Resource):
    
    _content_type = ContentType.SETTINGS
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
        super(Settings, self).__init__(resource, session)
        

class PersonalRecords(Resource):
    
    _content_type = ContentType.PERSONAL_RECORDS

    def __init__(self, resource, session=None):
        super(PersonalRecords, self).__init__(resource, session)

    def _parse_data(self, data):
        prop_dict = {}
        for actrecs in data:
            act_type = actrecs.get('activity_type')
            if act_type:
                act_stats = {}
                stats = actrecs.get('stats')
                if stats:
                    for stat in stats:
                        stat_type = stat['stat_type']
                        stat_val = stat['value']
                        stat_date = stat.get('date')
                        if stat_type == 'OVERALL':
                            act_stats[stat_type] = {'value': 
                                                    parse_distance(stat_val),}
                        else:
                            act_stats[stat_type] = {'value': 
                                                    parse_distance_km(stat_val),}
                        if stat_date is not None:
                            act_stats[stat_type]['date'] = stat_date
                    overall = act_stats.get('OVERALL')
                    if overall is not None and overall.get('value', 0) > 0:
                        prop_dict[act_type] = act_stats
            else:
                pass
        return prop_dict 


class FitnessActivityFeedItem(FeedItem):
    
    _prop_defs = {'start_time': parse_datetime,
                  'type': None,
                  'duration': None,
                  'total_distance': parse_distance_km,
                  'uri': PropResourceLink('FitnessActivity')}
    
    def __init__(self, data, session=None):
        super(FitnessActivityFeedItem, self).__init__(data, session)


class FitnessActivityIter(ResourceFeedIter):
    
    _content_type = ContentType.FITNESS_ACTIVITY_FEED
    _item_cls = FitnessActivityFeedItem
    
    def __init__(self, resource, session=None):
        super(FitnessActivityIter, self).__init__(resource, session)


class StrengthActivityFeedItem(FeedItem):
    
    _prop_defs = {'start_time': parse_datetime,
                  'uri': PropResourceLink('StrengthActivity')}
    
    def __init__(self, data, session=None):
        super(StrengthActivityFeedItem, self).__init__(data, session)


class StrengthActivityIter(ResourceFeedIter):
    
    _content_type = ContentType.STRENGTH_ACTIVITY_FEED
    _item_cls = StrengthActivityFeedItem
    
    def __init__(self, resource, session=None):
        super(StrengthActivityIter, self).__init__(resource, session)
        
