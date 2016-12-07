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

    def get_tzr_list(self, reg_bus_ent_id):
        # 投资人
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        # "http://qyxy.baic.gov.cn/xycx/queryCreditAction!tzrlist_all.dhtml?reg_bus_ent_id=DCBB0FD56D324C87AD672F5D35EA3437&ent_page=1&moreInfo=&newInv=newInv&fqr=&SelectPageSize=10&EntryPageNo=1&pageNo=1&pageSize=10&clear="
        # url = domain + "/xycx/queryCreditAction!tzrlist_all.dhtml?reg_bus_ent_id=%s&ent_page=1&clear=true&newInv=newInv&fqr=" % reg_bus_ent_id
        url = domain + "/xycx/queryCreditAction!tzrlist_all.dhtml?reg_bus_ent_id=%s&ent_page=1&moreInfo=&newInv=newInv&fqr=&SelectPageSize=100&EntryPageNo=1&pageNo=1&pageSize=100&clear=" % reg_bus_ent_id
        self._http_client.clear_cookies()
        response = self._verify_get(url, headers=headers, timeout=10)
        return response

    def get_tzr_history_list(self, reg_bus_ent_id):
        # 投资人历史
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%252F%2362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        # "http://qyxy.baic.gov.cn/xycx/queryCreditAction!tzrlist_hs_all.dhtml?reg_bus_ent_id=DCBB0FD56D324C87AD672F5D35EA3437&ent_page=1&moreInfo=&newInv=&fqr=&SelectPageSize=100&EntryPageNo=1&pageNo=1&pageSize=100&clear="
        # url = domain + "/xycx/queryCreditAction!tzrlist_hs_all.dhtml?reg_bus_ent_id=%s&ent_page=1&clear=true&fqr=" % reg_bus_ent_id
        url = domain + '/xycx/queryCreditAction!tzrlist_hs_all.dhtml?reg_bus_ent_id=%s&ent_page=1&moreInfo=&newInv=&fqr=&SelectPageSize=100&EntryPageNo=1&pageNo=1&pageSize=100&clear=' % reg_bus_ent_id
        self._http_client.clear_cookies()
        response = self._verify_get(url, headers=headers)
        return response

    def get_zyry_list(self, reg_bus_ent_id):
        # 重要人员
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%252F%; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        # "http://qyxy.baic.gov.cn/xycx/queryCreditAction!queryTzrxx_all.dhtml?reg_bus_ent_id=DCBB0FD56D324C87AD672F5D35EA3437&moreInfo=&SelectPageSize=100&EntryPageNo=1&pageNo=1&pageSize=100&clear="
        # url = domain + "/xycx/queryCreditAction!queryTzrxx_all.dhtml?reg_bus_ent_id=%s&clear=true" % reg_bus_ent_id
        url = domain + "/xycx/queryCreditAction!queryTzrxx_all.dhtml?reg_bus_ent_id=%s&moreInfo=&SelectPageSize=500&EntryPageNo=1&pageNo=1&pageSize=500&clear=true" % reg_bus_ent_id
        # url = domain + "/xycx/queryCreditAction!queryTzrxx_all.dhtml?reg_bus_ent_id=%s&moreInfo=&SelectPageSize=100&EntryPageNo=1&pageNo=1&pageSize=100&clear=" % reg_bus_ent_id
        self._http_client.clear_cookies()
        response = self._verify_get(url, headers=headers)
        return response

    def get_bgxx_list(self, reg_bus_ent_id):
        # 变更信息
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%%7C1477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        url = domain + "/newChange/newChangeAction!bgxx_view.dhtml?reg_bus_ent_id=%s" % reg_bus_ent_id
        self._http_client.clear_cookies()
        response = self._verify_get(url, headers=headers)
        return response

    def get_fzjg_list(self, reg_bus_ent_id):
        # 分支机构
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%252F%25F%7C1477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        url = domain + "/xycx/queryCreditAction!getEnt_Fzjgxx.dhtml?reg_bus_ent_id=%s&moreInfo=&SelectPageSize=100&EntryPageNo=1&pageNo=1&pageSize=100&clear=" % reg_bus_ent_id
        self._http_client.clear_cookies()
        response = self._verify_get(url, headers=headers)
        return response

    def get_ztzxx_list(self, reg_bus_ent_id):
        # 再投资信息
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        url = domain + "/xycx/queryCreditAction!getEnt_Ztzxx.dhtml?reg_bus_ent_id=%s&moreInfo=moreInfo&SelectPageSize=100&EntryPageNo=1&pageNo=1&pageSize=100&clear=true" % reg_bus_ent_id
        # url = domain + "/xycx/queryCreditAction!getEnt_Ztzxx.dhtml?reg_bus_ent_id=%s&moreInfo=moreInfo&SelectPageSize=10&EntryPageNo=1&pageNo=1&pageSize=10&clear=" % reg_bus_ent_id
        # url = domain + "/xycx/queryCreditAction!getEnt_Ztzxx.dhtml?reg_bus_ent_id=%s&moreInfo=&SelectPageSize=100&EntryPageNo=1&pageNo=1&pageSize=100&clear=" % reg_bus_ent_id
        self._http_client.clear_cookies()
        response = self._verify_get(url, headers=headers)
        return response

        # -----------------------------------------------level 3------------------------------------------------------- #
