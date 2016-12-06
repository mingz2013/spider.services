# -*- coding:utf-8 -*-
__author__ = 'zhaojm'


class Error302(Exception):
    def __init__(self):
        self.message = "error 302"
        pass


class Error403(Exception):
    def __init__(self):
        self.message = "error 403"
        pass


class Error404(Exception):
    def __init__(self):
        self.message = "error 404"
        pass


class Error502(Exception):
    def __init__(self):
        self.message = "error 502"
        pass


class Error503(Exception):
    def __init__(self):
        self.message = "error 503"
        pass


class ErrorStatusCode(Exception):
    def __init__(self, status_code):
        self.message = "error status code: %s" % status_code
        pass


class HttpClientError(Exception):
    def __init__(self):
        self.message = "http client error"
        pass


class MoreCheckverifyCodeTimesError(Exception):
    def __init__(self):
        self.message = "more check verify code times error"
        pass


class NeedrefreshProxyError(Exception):
    def __init__(self):
        # self._proxy_ip = proxy_ip
        # self._proxy_port = proxy_port
        self.message = "need refresh proxy error"
        pass


class NeedrefreshSearchKeyError(Exception):
    def __init__(self):
        # self._proxy_ip = proxy_ip
        # self._proxy_port = proxy_port
        self.message = "need refresh search key error"
        pass
