from enum import Enum


class method(Enum):
    # https://www.iana.org/assignments/http-methods/http-methods.xhtml
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    UPDATE = 'UPDATE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'
    SEARCH = 'SEARCH'
