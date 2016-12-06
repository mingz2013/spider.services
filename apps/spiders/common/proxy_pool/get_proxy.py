# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

# from mongo import ProxyDB
import logging
import time

from vpssshclient import VPSSSHClient


# class GetProxy(object):
#     def __init__(self):
#         self._proxy_cur = None
#         self.refresh_proxy()
#         pass
#
#     def refresh_proxy(self):
#         self._proxy_cur = ProxyDB.get_all()
#         if self._proxy_cur.count() == 0:
#             logging.info("proxy is empty, sleep 10 * 60s")
#             time.sleep(10 * 60)
#
#     def get_proxy(self):
#         try:
#             item = self._proxy_cur.next()
#             return item['ip'], item['port'], u'http'
#         except Exception, e:
#             self.refresh_proxy()
#             return self.get_proxy()
#
#     def remove_proxy(self, ip, port):
#         ProxyDB.remove_proxy(ip, port)

class GetProxy(object):
    def __init__(self, level, thread_id):
        # self._url = "http://123.206.6.251:8881/refresh_proxy/level_0"
        self._min_time_interval = 5
        self._last_request_time = -1
        # self._url = "http://123.206.6.251:8881/refresh_proxy/%s/%s" % (0, thread_id)
        self._vpnsshclient = VPSSSHClient()
        self._level = level
        self._thread_id = thread_id

    def _set_last_request_time(self):
        now = time.time()
        if now - self._last_request_time < self._min_time_interval:
            sleep = self._min_time_interval - (now - self._last_request_time)
            if sleep > 0:
                time.sleep(sleep)
            pass
        self._last_request_time = time.time()
        pass

    def refresh_proxy_level_thread(self, level, thread):
        level = int(level)
        thread = int(thread)
        num = 0
        if level == 0:
            if thread == 0:
                num = 0
            elif thread == 1:
                num = 1
            elif thread == 2:
                num = 2
            elif thread == 3:
                num = 5

        elif level == 1:
            if thread == 0:
                num = 3

        elif level == 2:
            if thread == 0:
                num = 4
        # elif level == 3:
        #     if thread == 0:
        #         num = 5
        else:
            raise Exception(level)
        logging.info("+++++++++++++++++++++%s:%s:%s+++++++++++++++++++" % (level, thread, num))
        proxy = self._vpnsshclient.refresh_proxy_ip(num)
        proxies = {"ip": proxy, "port": 5839, "type": "http"}
        # logging.info(request.headers['user-agent'] + "\nyour current ip is: " + request.remote_addr)
        # logging.info("write:-> %s" % proxies)
        # return json.dumps(proxies)
        # return proxy, 5839, u'http'
        return proxies

    def get_proxy(self):
        try:
            self._set_last_request_time()
            # response = requests.get(self._url)
            # if response.status_code != 200:
            #     raise Exception("status code error")
            # j = json.loads(response.content)
            j = self.refresh_proxy_level_thread(self._level, self._thread_id)
            return j["ip"], "%d" % j['port'], j['type']
        except Exception, e:
            logging.exception(e)
            return self.get_proxy()
