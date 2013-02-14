"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph).

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

The Health Graph API uses OAuth 2.0 for security. Every application must be registered 
with the Applications Portal of  Health Graph (http://runkeeper.com/partner). 
Once registered, the application will be assigned a unique client identifier and 
client secret for use with the Health Graph API.

"""

import content_type
from authmgr import AuthManager
from sessionmgr import Session, NullSession, init_session, get_session
from resources import (PersonalRecordType, ResourceLink,
                       User, Profile, Settings, PersonalRecords, 
                       FitnessActivity, FitnessActivitySummary, 
                       FitnessActivityFeedItem, FitnessActivityIter,
                       StrengthActivityFeedItem, StrengthActivityIter,
                       WeightMeasurementFeedItem, WeightMeasurementIter,)


__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.3.0"
__email__ = "aouyar at gmail.com"
__status__ = "Development"

