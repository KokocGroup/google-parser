# -*- coding:utf-8 -*-


class GoogleParserError(Exception):
    pass


class BadGoogleParserError(Exception):
    pass


class NoBodyInResponseError(GoogleParserError):
    pass


class EmptySerp(GoogleParserError):
    pass


class SnippetsParserException(GoogleParserError):
    pass


class BadUrlError(GoogleParserError):
    pass