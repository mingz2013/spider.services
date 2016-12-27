# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import random

from ssh_config import username, password, ssh_ip_list, proxy_port
from proxy_server import ProxyServer

from ..dbredis.proxy_server_pool import ProxyServerPoolRedis, pack_proxy_server, unpack_proxy_server


class ProxyServerPool(object):
    def __init__(self):
        pass

    @staticmethod
    def init_pool():
        proxy_server_list = []
        for item in ssh_ip_list:
            proxy_server = pack_proxy_server(item.get("ip"), item.get("port"))
            proxy_server_list.append(proxy_server)
        ProxyServerPoolRedis.init_proxy_server_pool(proxy_server_list)

    @staticmethod
    def request_one():
        proxy_server = ProxyServerPoolRedis.request_random_one_proxy_server()
        ip, port = unpack_proxy_server(proxy_server)
        p = ProxyServer(ip, port, username, password, proxy_port)
        return p

    @staticmethod
    def release_one(proxy_server):
        proxy_server_str = proxy_server.get_proxy_server_str()
        ProxyServerPoolRedis.release_proxy_server(proxy_server_str)
        pass

