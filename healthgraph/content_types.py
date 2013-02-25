"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module contains the definitions for Content Types used by Health Graph API.

"""


__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.3.0"
__email__ = "aouyar at gmail.com"
__status__ = "Development"

    
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
