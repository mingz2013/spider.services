# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import random

from ssh_config import username, password, ssh_ip_list
from proxy import Proxy


class ProxyPool(object):
    def __init__(self):
        self._username = username
        self._password = password
        self._proxy_list = []
        self._lock_list = []
        self._parse_ssh_list(ssh_ip_list)
        pass

    def _parse_ssh_list(self, ssh_list):
        for item in ssh_list:
            p = Proxy(item['ip'], item['port'])
            self._proxy_list.append(p)

    def request_one(self):
        if len(self._proxy_list) > 0:
            proxy = self._proxy_list[random.randint(len(self._proxy_list))]
            self._proxy_list.remove(proxy)
            self._lock_list.append(proxy)
            return proxy
        else:
            return None

    def release_one(self, proxy):
        self._proxy_list.append(proxy)
        self._lock_list.remove(proxy)
        pass
