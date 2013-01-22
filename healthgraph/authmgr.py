"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 
The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module implements the functions for authentication, authorization, revocation
of credentials for accesing the Health Graph API.

"""

import urllib
import json
import requests

__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.2.2"
__email__ = "aouyar at gmail.com"
__status__ = "Development"


api_authorization_url = 'https://runkeeper.com/apps/authorize'
api_deauthorization_url = 'https://runkeeper.com/apps/de-authorize'
api_access_token_url = 'https://runkeeper.com/apps/token'
rk_login_button_url = "http://static1.runkeeper.com/images/assets/login-%s-%s-%s.png"
rk_login_button_colors = ( 'blue', 'grey', 'black',)
rk_login_button_sizes = {200: '200x38',
                         300: '300x57',
                         600: '600x114',
                         None: '200x38',}
rk_login_caption_colors = ('white', 'black',)


class RunKeeperAuthMgr:
    """RunKeeper Authorization Manager
    
    Used for generating and revoking the Access Token for accessing RunKeeper
    using the Health Graph API. Once the Access Token is generated it can be
    stored and used for querying the HealthGraph API.
    
    """
    
    def __init__(self, client_id, client_secret, redirect_uri):
        """Initialize Authorization Manager.
        
        @param client_id:     Client ID for accessing Health Graph API
        @param client_secret: Client Secret for accessing Health Graph API
        @param redirect_uri:  Redirect URI for returning control to client web
                              application after the Authorization Dialog with
                              RunKeeper.com is executed successfully.
        
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
   
    def get_login_url(self, state=None):
        """Generates and returns URL for redirecting to Login Page of RunKeeper,
        which is the Authorization Endpoint of Health Graph API.
        
        @param state: State string. Passed to client web application at the end
                      of the Login Process.
        @return:      URL for redirecting to RunKeeper Login Page.  
        
        """
        payload = {'response_type': 'code',
                   'client_id': self._client_id,
                   'redirect_uri': self._redirect_uri,}
        if state is not None:
            payload['state'] = state
        return "%s?%s" % (api_authorization_url,
                          urllib.urlencode(payload))
    
    def get_login_button_url(self, button_color=None, caption_color=None, button_size=None):
        """Return URL for image used for RunKeeper Login button.
        
        @param button_color:  Button color. Either 'blue', 'grey' or 'black'.
                              Default: 'blue'.
        @param caption_color: Button text color. Either 'white' or 'black'.
                              Default: 'white'
        @param button_size:   Button width in pixels. Either 200, 300 or 600.
                              Default: 200
        @return:              URL for Login Button Image.
        
        """
        if not button_color in rk_login_button_colors:
            button_color = rk_login_button_colors[0]
        if not caption_color in rk_login_caption_colors:
            caption_color = rk_login_caption_colors[0]
        if rk_login_button_sizes.has_key(button_size):
            button_size = rk_login_button_sizes[button_size]
        else:
            button_size = rk_login_button_sizes['None']
        return rk_login_button_url % (button_color, caption_color, button_size)
        
    def get_access_token(self, code):
        """Returns Access Token retrieved from the Health Graph API Token 
        Endpoint following the login to RunKeeper.
        to RunKeeper. 
        
        @param code: Code returned by Health Graph API at the Authorization or
                     RunKeeper Login phase.
        @return:     Access Token for querying the Health Graph API.
        
        """
        payload = {'grant_type': 'authorization_code',
                   'code': code,
                   'client_id': self._client_id,
                   'client_secret': self._client_secret,
                   'redirect_uri': self._redirect_uri,}
        req = requests.post(api_access_token_url, data=payload)
        data = json.loads(req.text)
        return data.get('access_token')
    
    def revoke_access_token(self, access_token):
        """Revokes the Access Token by accessing the De-authorization Endpoint
        of Health Graph API.
        
        @param access_token: Access Token for querying Health Graph API.
        
        """
        payload = {'access_token': access_token,}
        req = requests.post(api_deauthorization_url, data=payload) #@UnusedVariable
        