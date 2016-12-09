# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from ssh_config import username, password, ssh_ip_list


class ProxyPool(object):
    def __init__(self):
        self._username = username
        self._password = password
        self._sss_config = ssh_ip_list
        pass

    def request_one(self):
        pass

    def release_one(self):
        pass
