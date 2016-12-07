# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging

from ..common.base_site_client import BaseSiteClient
from ..common.utils import get_timeStamp


class SiteClient(BaseSiteClient):
    def __init__(self, config, proxies):
        BaseSiteClient.__init__(config, proxies)

        self.credit_ticket = None
        self.currentTimeMillis = None
        self._detail_url = None
        self._index_1_url = None
        self._index_2_url = None
        self._search_list_url = None
        self._qynb_detail_url = None
        pass

    # -----------------------------------------------level 1------------------------------------------------------- #
    def get_qynb_list(self, reg_bus_ent_id):
        # 企业年报

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': self._config.host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }

        url = self._config.domain + "/entPub/entPubAction!getTabForNB_new.dhtml?entId=%s&flag_num=0&clear=true&timeStamp=%s" % (
            reg_bus_ent_id, get_timeStamp())
        logging.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logging.info(url)
        logging.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        self._http_client.clear_cookies()
        response = self._verify_get(url, headers=headers)
        return response

    def get_qynb_detail(self, url):
        # 企业年报详细信息
        self._qynb_detail_url = url
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': self._config.host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }

        response = self._verify_get(url, headers=headers)
        return response

    def get_qynb_gdcz_list(self, url):
        # 股东出资
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A7463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': self._config.host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }

        response = self._verify_get(url, headers=headers)
        return response

    def get_qynb_dwdb_list(self, url):
        # 对外提供保证担保信息
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%%7C1477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': self._config.host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }

        response = self._verify_get(url, headers=headers)
        return response

    def get_qynb_wz_list(self, url):
        # 网站
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A7C1477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': self._config.host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        response = self._verify_get(url, headers=headers)
        return response

    def get_qynb_xgjl_list(self, url):
        # 修改记录
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': self._config.host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        response = self._verify_get(url, headers=headers)
        return response

    def get_qynb_dwtz_list(self, url):
        # 对外投资
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%251477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': self._config.host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        response = self._verify_get(url, headers=headers)
        return response

    def get_qynb_gdbg_list(self, url):
        # 股东变更
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': self._config.host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        response = self._verify_get(url, headers=headers)
        return response