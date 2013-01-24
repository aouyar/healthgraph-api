"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module defines the exceptions used by the API.

"""


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
    """Raised when remote API end-point access is attempted before completing
    initialization of session.
    
    """
    pass

