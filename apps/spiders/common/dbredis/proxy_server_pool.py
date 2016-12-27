# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from . import redis_client

redis_proxy_server_pool_key = "proxy.server.pool"
redis_proxy_server_used_key = "proxy.server.used"


def pack_proxy_server(ip, port):
    return "%s:%s" % (ip, port)


def unpack_proxy_server(proxy_server):
    ip, port = proxy_server.split(':')
    return ip, port


class ProxyServerPoolRedis(object):
    def __init__(self):
        pass

    @staticmethod
    def request_random_one_proxy_server():
        v = redis_client.brpoplpush(redis_proxy_server_pool_key, redis_proxy_server_used_key)
        return v

    @staticmethod
    def release_proxy_server(proxy_server):
        p = redis_client.pipeline()
        p.lrem(redis_proxy_server_used_key, 0, proxy_server)
        p.lpush(redis_proxy_server_pool_key, proxy_server)
        p.execute()
        pass

    @staticmethod
    def init_proxy_server_pool(proxy_server_list):
        p = redis_client.pipeline()
        p.delete(redis_proxy_server_pool_key)
        p.delete(redis_proxy_server_used_key)
        p.lpush(redis_proxy_server_pool_key, proxy_server_list)
        p.execute()
        pass
