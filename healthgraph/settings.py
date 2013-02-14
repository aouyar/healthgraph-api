"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module stores the global constants used by the Health Graph Client.

"""

__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.3.0"
__email__ = "aouyar at gmail.com"
__status__ = "Development"


API_AUTHORIZATION_URL = 'https://runkeeper.com/apps/authorize'
API_DEAUTHORIZATION_URL = 'https://runkeeper.com/apps/de-authorize'
API_ACCESS_TOKEN_URL = 'https://runkeeper.com/apps/token'
LOGIN_BUTTON_URL = "http://static1.runkeeper.com/images/assets/login-%s-%s-%s.png"
LOGIN_BUTTON_COLORS = ( 'blue', 'grey', 'black',)
LOGIN_BUTTON_SIZES = {200: '200x38',
                      300: '300x57',
                      600: '600x114',
                      None: '200x38',}
LOGIN_BUTTON_CAPTION_COLORS = ('white', 'black',)

API_URL = 'https://api.runkeeper.com'
USER_RESOURCE = '/user'
DEFAULT_PAGE_SIZE = 25

NUM2MONTH = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
             'Nov','Dec',)
MONTH2NUM = dict(zip(NUM2MONTH,range(1,13)))