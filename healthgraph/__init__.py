"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 
The API is used for accessing RunKeeper.com (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

"""

import requests

__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Ali Onur Uyar"
__email__ = "aouyar at gmail.com"
__status__ = "Development"


api_authorization_url = 'https://runkeeper.com/apps/authorize'
api_deauthorization_url = 'https://runkeeper.com/apps/de-authorize'
api_access_token_url = 'https://runkeeper.com/apps/token'
api_url = 'https://api.runkeeper.com'
api_user_resource = '/user'
rk_login_button_url = "http://static1.runkeeper.com/images/assets/login-%s-%s-%s.png"
rk_login_button_colors = ( 'blue', 'grey', 'black',)
rk_login_button_sizes = {200: '200x38',
                         300: '300x57',
                         600: '600x114',
                         None: '200x38',}
rk_login_caption_colors = ('white', 'black',)


class RunKeeperAuthMgr:
    
    def __init__(self, client_id, client_secret, redirect_uri):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
   
    def getLoginURL(self, state=None):
        payload = {'response_type': 'code',
                   'client_id': self._client_id,
                   'redirect_uri': self._redirect_uri,}
        if state is not None:
            payload['state'] = state
        req = requests.Request(api_authorization_url, params=payload)
        return req.full_url
    
    def getLoginButtonURL(self, button_color=None, caption_color=None, 
                            button_size=None):
        if not button_color in rk_login_button_colors:
            button_color = rk_login_button_colors[0]
        if not caption_color in rk_login_caption_colors:
            caption_color = rk_login_caption_colors[0]
        if rk_login_button_sizes.has_key(button_size):
            button_size = rk_login_button_sizes[button_size]
        else:
            button_size = rk_login_button_sizes['None']
        return rk_login_button_url % (button_color, caption_color, button_size)
        
    def getAccessToken(self, code):
        payload = {'grant_type': 'authorization_code',
                   'code': code,
                   'client_id': self._client_id,
                   'client_secret': self._client_secret,
                   'redirect_uri': self._redirect_uri,}
        req = requests.post(api_access_token_url, data=payload)
        return req.json['access_token']
    
    def rmAccessToken(self, access_token):
        payload = {'access_token': access_token,}
        req = requests.post(api_deauthorization_url, data=payload) #@UnusedVariable
    
    
class RunKeeperClient:
    
    def __init__(self, access_token):
        self._access_token = access_token
        self._root = None
        
    def _apiRequest(self, request_type, resource='user', 
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
                    self._root = self.getRoot()
                path = self._root.get(resource)
                if path is None:
                    pass # TODO - Raise Error for invalid resource type.
        url = api_url + path
        req = requests.request(request_type, url, headers=headers, params=params)
        # TODO - Check request errors.
        return req.json
    
    def getRoot(self):
        resource = 'user'
        content_type = 'User'
        return self._apiRequest('GET', resource, content_type)
        
    def getProfile(self):
        resource = 'profile'
        content_type = 'Profile'
        return self._apiRequest('GET', resource, content_type)
    
    def getSettings(self):
        resource = 'settings'
        content_type = 'Settings'
        return self._apiRequest('GET', resource, content_type)
        
    def getActivityList(self):
        resource = 'fitness_activities'
        content_type = 'FitnessActivityFeed'
        return self._apiRequest('GET', resource, content_type)
    
    def getActivitySummary(self, activity_id):
        content_type = 'FitnessActivitySummary'
        return self._apiRequest('GET', activity_id, content_type)
    
    def getActivity(self, resource):
        content_type = 'FitnessActivity'
        return self._apiRequest('GET', resource, content_type)
    
    def getWeightMeasurements(self):
        resource = 'weight'
        content_type = 'WeightSetFeed'
        return self._apiRequest('GET', resource, content_type)
    
    def getWeightMeasurement(self, resource):
        content_type = 'WeightSet'
        return self._apiRequest('GET', resource, content_type)
    
    def getRecords(self):
        resource = 'records'
        content_type = 'Records'
        resp = self._apiRequest('GET', resource, content_type)
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
    