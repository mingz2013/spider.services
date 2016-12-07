# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging

from http_client import HTTPClient

from exception import Error302, Error403, Error404, Error502, Error503, ErrorStatusCode, HttpClientError

import random


class BaseSiteClient(object):
    def __init__(self, config, proxies={}):
        self._config = config
        self._http_client = HTTPClient(proxies=proxies)
        self._user_agent = random.choice(self._config.user_agents)

        pass

    def _check_response(self, response):
        if response.status_code == 200:
            logging.debug(response.headers)
            pass
        elif response.status_code == 302:
            location = response.headers['Location']
            logging.debug("location: %s" % location)
            raise Error302()
        elif response.status_code == 403:
            raise Error403()
        elif response.status_code == 404:
            raise Error404()
        elif response.status_code == 502:
            raise Error502()
        elif response.status_code == 503:
            raise Error503()
        else:
            raise ErrorStatusCode(response.status_code)
        return response

    def _verify_post(self, url, data=None, json=None, times=0, headers=None, timeout=None):
        if not headers:
            headers = self._config.default_headers
        if not timeout:
            timeout = self._config.default_timeout

        headers.update({
            'User-Agent': self._user_agent,
            # "Proxy-Authorization": self.get_authHeader()
        })

        try:
            response = self._http_client.post(url=url, data=data, json=json, headers=headers, timeout=timeout)
            return self._check_response(response)
        except Error403, err:
            raise err
        except HttpClientError, err:
            times += 1
            if times < 2:
                return self._verify_post(url, data=data, json=json, times=times, headers=headers, timeout=timeout)
            else:
                raise err

    def _verify_get(self, url, times=0, headers=None, timeout=None):
        if not headers:
            headers = self._config.default_headers
        if not timeout:
            timeout = self._config.default_timeout

        headers.update({
            'User-Agent': self._user_agent,
            # "Proxy-Authorization": self.get_authHeader()
        })

        try:
            response = self._http_client.get(url, headers=headers, timeout=timeout)
            return self._check_response(response)
        except Error403, err:
            raise err
        except HttpClientError, err:
            times += 1
            if times < 2:
                return self._verify_get(url, times=times, headers=headers, timeout=timeout)
            else:
                raise err
