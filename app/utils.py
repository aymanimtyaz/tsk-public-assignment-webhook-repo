"""
This module contains an assortment of various utility classes and 
functions that can be imported and used where needed.

Classes
-------
GithubEvent

Functions
---------
format_datetime(datetime_string)
"""

import datetime

class GithubEvent:
    """
    This class represents a GitHub event.

    Attributes
    ----------
    _id: str, default None
        The string representation of the event's mongodb oid, if 
        applicable.
    request_id: str
        Github assigned unique identifier for an event.
    author: str
        The person who initiated the event.
    action: str
        The type of event. 'MERGE', 'PUSH', or 'PULL_REQUEST'.
    from_branch: str
        The name of the Git branch on the left hand side.
    to_branch: str
        The name of the Git branch on the right hand side.
    timestamp: str
        The UTC datetime string representing the time of event.

    Methods
    -------
    object_to_dict()
        Returns the dict/json representation of event objects.
    """

    def __init__(
            self, request_id, author, action, from_branch, 
            to_branch, timestamp, _id=None):
        """
        Initializes a GithubEvent object

        the '_id' parameter, representing a mongodb oid, will only be 
        non-empty if the event is being initialized from a mongodb 
        document, otherwise, it will default to None.

        Parameters
        ----------
        _id: str, default None
            The string representation of the event's mongodb oid, if 
            applicable.
        request_id: str
            Github assigned unique identifier for an event.
        author: str
            The person who initiated the event.
        action: str
            The type of event. 'MERGE', 'PUSH', or 'PULL_REQUEST'.
        from_branch: str
            The name of the Git branch on the left hand side.
        to_branch: str
            The name of the Git branch on the right hand side.
        timestamp: str
            The UTC datetime string representing the time of event.
        """
        self._id = _id
        self.request_id = request_id
        self.author = author
        self.action = action
        self.from_branch = from_branch
        self.to_branch = to_branch
        self.timestamp = timestamp

    def event_object_to_dict(self):
        """ Returns the dict/json representation of event objects.

        If the event has been initialized from a document retrieved 
        from mongodb, it will have a non-empty'_id' field. Otherwise,
        if the event hasn't been retrieved from mongodb and is being 
        initialized for the first time, it's '_id' field will be none 
        and it won't be added in the event's dict/json representation. 
        """
        event_dict = {
            "request_id":self.request_id,
            "author":self.author,
            "action":self.action,
            "from_branch":self.from_branch,
            "to_branch":self.to_branch,
            "timestamp":self.timestamp
        }
        if self._id:
            event_dict["_id"] = self._id
        return event_dict


def format_datetime(datetime_string):
    """
    Takes a UTC datetime string and returns it in the required format.

    The datetime_string argument passed to the function must be in the 
    following format: (%Y-%m-%d %H:%M:%S) and is assumed to be in UTC. 
    The datetime is formatted and returned as 
    (%-d(st/nd/rd/th) %B %Y - %I:%M %p UTC).

    Parameters
    ----------
    datetime_string: str
        A UTC datetime string

    Returns
    -------                   
    formatted_datetime_string: str
        A formatted UTC datetime string
    """
    INPUT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    REQUIRED_DATETIME_FORMAT = "%-d %B %Y - %I:%M %p UTC"

    # convert input datetime string to python datetime
    input_datetime = datetime.datetime.strptime(
        datetime_string, 
        INPUT_DATETIME_FORMAT)

    # convert the python datetime to the required string format
    input_datetime_string = datetime.datetime.strftime(
        input_datetime, 
        REQUIRED_DATETIME_FORMAT)

    # get the components from the formatted datetime string
    input_datetime_components = input_datetime_string.split(" ")

    # append the appropriate suffix to the date component
    if (4 <= int(input_datetime_components[0]) <= 20 or 
            24 <= int(input_datetime_components[0]) <= 30):
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][int(input_datetime_components[0])%10 - 1]
    input_datetime_components[0] += suffix

    # rejoin all the components to get the required datetime string
    formatted_datetime_string =  " ".join(input_datetime_components)

    return formatted_datetime_string