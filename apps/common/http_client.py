# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging
import random
import time

import requests

from config import download_delay, default_headers, download_timeout, USER_AGENTS
from exception import HttpClientError


class HTTPClient(object):
    def __init__(self, min_time_interval=download_delay, proxies={}):
        self._session = requests.Session()
        self._session.headers.update(default_headers)
        self._session.headers.update({"User-Agent": random.choice(USER_AGENTS)})
        self._min_time_interval = min_time_interval + 1 * random.random()
        self._last_request_time = -1

        self._current_proxies = proxies

        pass

    def _set_last_request_time(self):
        now = time.time()
        if now - self._last_request_time < self._min_time_interval:
            sleep = self._min_time_interval - (now - self._last_request_time)
            if sleep > 0:
                time.sleep(sleep)
            pass
        self._last_request_time = time.time()
        pass

    def post(self, url, data=None, json=None, headers=default_headers, timeout=download_timeout):
        self._set_last_request_time()

        logging.info("<POST %s> %s" % (url, data))
        # logging.debug("HEADER %s" % self._session.headers)
        # logging.debug(self._current_proxies)
        # logging.debug(headers)
        # logging.debug(self._session.cookies)
        try:
            response = self._session.post(url, data=data, json=json, proxies=self._current_proxies,
                                          timeout=timeout, headers=headers,
                                          # allow_redirects=False
                                          )
        except Exception, e:
            logging.error(e.message)
            raise HttpClientError()
        logging.info("<response %d>" % response.status_code)

        return response

    def get(self, url, headers=default_headers, timeout=download_timeout):
        self._set_last_request_time()

        logging.info("<GET %s>" % url)
        # logging.debug("HEADER %s" % self._session.headers)
        # logging.debug(self._current_proxies)
        # logging.debug(headers)
        # logging.debug(self._session.cookies)
        try:
            response = self._session.get(url, proxies=self._current_proxies,
                                         timeout=timeout, headers=headers,
                                         # allow_redirects=False
                                         )
        except Exception, e:
            logging.error(e.message)
            raise HttpClientError()
        logging.info("<response %d>" % response.status_code)

        return response
