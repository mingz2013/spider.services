# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import random

from ssh_config import username, password, ssh_ip_list, proxy_port
from proxy_server import ProxyServer


class ProxyServerPool(object):
    def __init__(self):
        self._proxy_server_list = []
        self._lock_list = []
        self._parse_ssh_list(ssh_ip_list)
        pass

    def _parse_ssh_list(self, ssh_list):
        for item in ssh_list:
            p = ProxyServer(item['ip'], item['port'], username, password, proxy_port)
            self._proxy_server_list.append(p)

    def request_one(self):
        if len(self._proxy_server_list) > 0:
            proxy = self._proxy_server_list[random.randint(len(self._proxy_server_list))]
            self._proxy_server_list.remove(proxy)
            self._lock_list.append(proxy)
            return proxy
        else:
            return None

    def release_one(self, proxy_server):
        self._proxy_server_list.append(proxy_server)
        self._lock_list.remove(proxy_server)
        pass
