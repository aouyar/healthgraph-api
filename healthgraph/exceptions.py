"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module defines the exceptions used by the API.

"""


__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.3.0"
__email__ = "aouyar at gmail.com"
__status__ = "Development"


class Error(Exception):
    """Base class for exceptions in this module"""
    pass


class ClientError(Error):
    """Errors on client side."""
    pass


class RemoteError(Error):
    """Errors on remote end"""
    pass


class NoSessionError(Error):
    """Raised when remote API end-point access is attempted before initialization 
    of session.
    
    """
    pass


class ParseError(Error):
    """Error in parsing data returned by API.
    
    """
    pass


class ParseValueError(Error):
    """Error in parsing value returned by API.
    
    """
    pass


class ParseParamError(Error):
    """Error in parsing parameter passed to API.
    
    """
    pass

