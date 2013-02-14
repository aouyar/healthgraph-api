"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module implements the functions for authentication, authorization, revocation
of credentials for accesing the Health Graph API.

"""

import urllib
import requests
import settings

__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.3.0"
__email__ = "aouyar at gmail.com"
__status__ = "Development"


class AuthManager(object):
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
        return "%s?%s" % (settings.API_AUTHORIZATION_URL,
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
        if not button_color in settings.LOGIN_BUTTON_COLORS:
            button_color = settings.LOGIN_BUTTON_COLORS[0]
        if not caption_color in settings.LOGIN_BUTTON_CAPTION_COLORS:
            caption_color = settings.LOGIN_BUTTON_CAPTION_COLORS[0]
        if settings.LOGIN_BUTTON_SIZES.has_key(button_size):
            button_size = settings.LOGIN_BUTTON_SIZES[button_size]
        else:
            button_size = settings.LOGIN_BUTTON_SIZES['None']
        return settings.LOGIN_BUTTON_URL % (button_color, 
                                            caption_color, 
                                            button_size)
        
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
        req = requests.post(settings.API_ACCESS_TOKEN_URL, data=payload)
        data = req.json()
        return data.get('access_token')
    
    def revoke_access_token(self, access_token):
        """Revokes the Access Token by accessing the De-authorization Endpoint
        of Health Graph API.
        
        @param access_token: Access Token for querying Health Graph API.
        
        """
        payload = {'access_token': access_token,}
        req = requests.post(settings.API_DEAUTHORIZATION_URL, data=payload) #@UnusedVariable
        