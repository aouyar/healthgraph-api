"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module stores the global constants used by the Health Graph Client.

"""


RK_API_AUTHORIZATION_URL = 'https://runkeeper.com/apps/authorize'
RK_API_DEAUTHORIZATION_URL = 'https://runkeeper.com/apps/de-authorize'
RK_API_ACCESS_TOKEN_URL = 'https://runkeeper.com/apps/token'
RK_LOGIN_BUTTON_URL = "http://static1.runkeeper.com/images/assets/login-%s-%s-%s.png"
RK_LOGIN_BUTTON_COLORS = ( 'blue', 'grey', 'black',)
RK_LOGIN_BUTTON_SIZES = {200: '200x38',
                         300: '300x57',
                         600: '600x114',
                         None: '200x38',}
RK_LOGIN_BUTTON_CAPTION_COLORS = ('white', 'black',)

RK_API_URL = 'https://api.runkeeper.com'
RK_USER_RESOURCE = '/user'
