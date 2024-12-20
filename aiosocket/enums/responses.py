from enum import Enum


class Responses(Enum):
    """
    Enum for response types
    """

    RESPONSE = "response"
    ERROR = "error"


class ServerResponses(Enum):
    """
    Enum for server responses
    """

    OK = "ok"
    ERROR = "error"
    INTERNAL_ERROR = "internal_error"
    NOT_FOUND = "not_found"
    CANT_REACH_SERVER = "cant_reach_server"
