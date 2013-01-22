"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 
The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module implements the functionality for for retrieving, updating, deleting 
and uploading Fitness Activity and Health Measurements Information using the
Health Graph API.

"""

import json
import requests

__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.2.2"
__email__ = "aouyar at gmail.com"
__status__ = "Development"


api_url = 'https://api.runkeeper.com'
api_user_resource = '/user'


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
    
    
class RunKeeperClient:
    
    def __init__(self, access_token):
        self._access_token = access_token
        self._root = None
        
    def _api_request(self, request_type, resource='user', 
                    content_type=None, params=None):
        headers = {'Authorization': "Bearer %s" % self._access_token,}
        content_header = None
        if content_type is not None:
            if request_type == 'GET':
                content_header = 'Accept'
            elif request_type in ('POST', 'PUT'):
                content_header = 'Content-Type'
            else:
                content_header = None
            if content_header is not None:
                headers[content_header] = ('application/vnd.com.runkeeper.%s+json'
                                           % content_type)
        if resource.startswith('/'):
            path = resource
        else:
            if resource == 'user':
                path = api_user_resource
            else:
                if self._root is None:
                    self._root = self.get_root()
                path = self._root.get(resource)
                if path is None:
                    pass # TODO - Raise Error for invalid resource type.
        url = api_url + path
        req = requests.request(request_type, url, headers=headers, params=params)
        # TODO - Check request errors.
        data = json.loads(req.text)
        return data
    
    def get_root(self):
        resource = 'user'
        content_type = 'User'
        return self._api_request('GET', resource, content_type)
        
    def get_profile(self):
        resource = 'profile'
        content_type = 'Profile'
        return self._api_request('GET', resource, content_type)
    
    def get_settings(self):
        resource = 'settings'
        content_type = 'Settings'
        return self._api_request('GET', resource, content_type)
        
    def get_activity_list(self, page_size=10):
        resource = 'fitness_activities'
        content_type = 'FitnessActivityFeed'
        return self._api_request('GET', resource, content_type, 
                                params={'pageSize': page_size,})

    def get_activity(self, resource, summary=False):
        if summary:
            content_type = 'FitnessActivitySummary'
        else:
            content_type = 'FitnessActivity'
        return self._api_request('GET', resource, content_type)
    
    def get_weight_measurements(self, page_size=10):
        resource = 'weight'
        content_type = 'WeightSetFeed'
        return self._api_request('GET', resource, content_type,
                                params={'pageSize': page_size,})
    
    def get_weight_measurement(self, resource):
        content_type = 'WeightSet'
        return self._api_request('GET', resource, content_type)
    
    def get_records(self):
        resource = 'records'
        content_type = 'Records'
        resp = self._api_request('GET', resource, content_type)
        result = {}
        for actrecs in resp:
            act_type = actrecs.get('activity_type')
            if act_type:
                act_stats = {}
                stats = actrecs.get('stats')
                if stats:
                    for stat in stats:
                        act_stats[stat['stat_type']] = stat['value']
                if act_stats.get('OVERALL', 0) > 0:
                    result[act_type] = act_stats
        return result
    