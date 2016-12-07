# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging

# import time
# import urllib2

from http_client import HTTPClient
from utils import get_timeStamp

from exception import Error302, Error403, Error404, Error502, Error503, ErrorStatusCode, HttpClientError, \
    NeedrefreshProxyError
from config import default_headers, USER_AGENTS
import random
from config import host, domain, download_timeout


class SiteClient(object):
    def __init__(self, proxies={}):
        # self._username = username
        # self._password = password
        self._http_client = HTTPClient(proxies=proxies)
        self._user_agent = random.choice(USER_AGENTS)

        self.credit_ticket = None
        self.currentTimeMillis = None
        self._detail_url = None
        self._index_1_url = None
        self._index_2_url = None
        self._search_list_url = None

        self._qynb_detail_url = None
        pass

    # -----------------------------------------------get post------------------------------------------------------- #
    def _verify_post(self, url, data=None, json=None, times=0, headers=default_headers, timeout=download_timeout):

        headers.update({
            'User-Agent': self._user_agent,
            # "Proxy-Authorization": self.get_authHeader()
        })

        try:
            response = self._http_client.post(url=url, data=data, json=json, headers=headers, timeout=timeout)
            if response.status_code == 200:
                logging.debug(response.headers)
                pass
            elif response.status_code == 302:
                location = response.headers['Location']
                logging.debug("location: %s" % location)
                raise NeedrefreshProxyError()
            elif response.status_code == 403:
                raise Error403()
            elif response.status_code == 404:
                raise NeedrefreshProxyError()
            elif response.status_code == 502:
                raise NeedrefreshProxyError()
            elif response.status_code == 503:
                raise NeedrefreshProxyError()
            else:
                raise ErrorStatusCode(response.status_code)
            if response.content.find('繁访问错误页面') > 0:
                logging.info("---------------||||||||||||||||||||||||-------------")
                raise NeedrefreshProxyError()
            return response
        except Error403, err:
            raise err
        except HttpClientError, err:
            times += 1
            if times < 2:
                return self._verify_post(url, data=data, json=json, times=times, headers=headers, timeout=timeout)
            else:
                raise err

    def _verify_get(self, url, times=0, headers=default_headers, timeout=download_timeout):
        headers.update({
            'User-Agent': self._user_agent
        })
        try:
            response = self._http_client.get(url, headers=headers, timeout=timeout)
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
            else:
                raise ErrorStatusCode(response.status_code)
            if response.content.find('繁访问错误页面') > 0:
                logging.info("---------------||||||||||||||||||||||||-------------")
                raise NeedrefreshProxyError()
            return response
        except Error403, err:
            raise err
        except HttpClientError, err:
            times += 1
            if times < 2:
                return self._verify_get(url, times=times, headers=headers, timeout=timeout)
            else:
                raise err

    # -----------------------------------------------level 0------------------------------------------------------- #
    # -------------right main----------------------------
    # def get_detail(self, reg_bus_ent_id, credit_ticket):
    #     # 公司详情页面
    #     url = domain + "/xycx/queryCreditAction!qyxq_view.dhtml?reg_bus_ent_id=%s&credit_ticket=%s" % (
    #         reg_bus_ent_id, credit_ticket)
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate, sdch',
    #         'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
    #         'Cache-Control': 'no-cache',
    #         'Connection': 'keep-alive',
    #         # 'Content-Length': '47',
    #         # 'Content-Type': 'application/x-www-form-urlencoded',
    #         # 'Cookie': '',
    #         'Host': host,
    #         # 'Origin': '',
    #         'Pragma': 'no-cache',
    #         'Referer': self._search_list_url,
    #         'Upgrade-Insecure-Requests': '1',
    #     }
    #     response = self._verify_get(url, headers=headers)
    #     self._detail_url = url
    #     return response

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
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }

        url = domain + "/entPub/entPubAction!getTabForNB_new.dhtml?entId=%s&flag_num=0&clear=true&timeStamp=%s" % (
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
            'Host': host,
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
            'Host': host,
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
            'Host': host,
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
            'Host': host,
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
            'Host': host,
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
            'Host': host,
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
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'Referer': self._qynb_detail_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        response = self._verify_get(url, headers=headers)
        return response

    # -----------------------------------------------level 2------------------------------------------------------- #








    # -----------left main-----------------------------
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







    def get_gdcz_list(self, reg_bus_ent_id):
        # 股东出资
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 2F%7C1477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        url = domain + "/newChange/newChangeAction!getTabForNB_new.dhtml?entId=%s&flag_num=1&clear=true&timeStamp=%s" % (
            reg_bus_ent_id, get_timeStamp())
        self._http_client.clear_cookies()
        response = self._verify_get(url, headers=headers)
        return response

    def get_gqbg_list(self, reg_bus_ent_id):
        # 股权变更信息
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%252F%277463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        url = domain + "/newChange/newChangeAction!getTabForNB_new.dhtml?entId=%s&flag_num=2&clear=true&timeStamp=%s" % (
            reg_bus_ent_id, get_timeStamp())
        self._http_client.clear_cookies()
        response = self._verify_get(url, headers=headers)
        return response

    def get_xzxk_list(self, reg_bus_ent_id):
        # 行政许可
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%252F%7C1477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        url = domain + "/newChange/newChangeAction!getTabForNB_new.dhtml?entId=%s&flag_num=3&clear=true&timeStamp=%s" % (
            reg_bus_ent_id, get_timeStamp())
        self._http_client.clear_cookies()
        response = self._verify_get(url, headers=headers)
        return response

    def get_zscq_list(self, reg_bus_ent_id):
        # 知识产权
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%252F%%7C1477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        url = domain + "/newChange/newChangeAction!getTabForNB_new.dhtml?entId=%s&flag_num=4&clear=true&timeStamp=%s" % (
            reg_bus_ent_id, get_timeStamp())
        self._http_client.clear_cookies()
        response = self._verify_get(url, headers=headers)
        return response

    def get_xzcf_list(self, reg_bus_ent_id):
        # 行政处罚
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%252F%252252F%7C1477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        url = domain + "/newChange/newChangeAction!getTabForNB_new.dhtml?entId=%s&flag_num=5&clear=true&timeStamp=%s" % (
            reg_bus_ent_id, get_timeStamp())
        self._http_client.clear_cookies()
        response = self._verify_get(url, headers=headers)
        return response

    # -----------------------------------------------level 4------------------------------------------------------- #
    # -------------其他信息------------------------------------
    def get_jsxx_list(self, reg_bus_ent_id):
        # 警示信息
        headers = {
            'Accept': 'text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%252%7C1477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Origin': domain,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': domain + '/xycx/queryCreditAction!qyxq_view.dhtml?reg_bus_ent_id=DCBB0FD56D324C87AD672F5D35EA3437&credit_ticket=AFD334549753B8FB11986D8C347561F2',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }

        url = domain + "/newChange/newChangeAction!getGj.dhtml"
        form_data = {
            "info_categ": "04",
            "reg_bus_ent_id": reg_bus_ent_id,
            "vchr_bmdm": "",
            "ent_name": "",
            "random": "%s" % random.random()
        }
        self._http_client.clear_cookies()
        response = self._verify_post(url, form_data, headers=headers)
        return response

    def get_tsxx_list(self, reg_bus_ent_id):
        # 提示信息
        headers = {
            'Accept': 'text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%252F%25C1477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Origin': domain,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': domain + '/xycx/queryCreditAction!qyxq_view.dhtml?reg_bus_ent_id=DCBB0FD56D324C87AD672F5D35EA3437&credit_ticket=AFD334549753B8FB11986D8C347561F2',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        url = domain + "/newChange/newChangeAction!getGj.dhtml"
        form_data = {
            "info_categ": "03",
            "reg_bus_ent_id": reg_bus_ent_id,
            "vchr_bmdm": "",
            "ent_name": "",
            "random": "%s" % random.random()
        }
        self._http_client.clear_cookies()
        response = self._verify_post(url, form_data, headers=headers)
        return response

    def get_lhxx_list(self, reg_bus_ent_id):
        # 良好信息
        headers = {
            'Accept': 'text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%252F%; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Origin': domain,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': domain + '/xycx/queryCreditAction!qyxq_view.dhtml?reg_bus_ent_id=DCBB0FD56D324C87AD672F5D35EA3437&credit_ticket=AFD334549753B8FB11986D8C347561F2',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        url = domain + "/newChange/newChangeAction!getGj.dhtml"
        form_data = {
            "info_categ": "02",
            "reg_bus_ent_id": reg_bus_ent_id,
            "vchr_bmdm": "",
            "ent_name": "",
            "random": "%s" % random.random()
        }
        self._http_client.clear_cookies()
        response = self._verify_post(url, form_data, headers=headers)
        return response

    def get_xkzzxx_list(self, reg_bus_ent_id):
        # 许可资质信息
        headers = {
            'Accept': 'text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%252F%22F%7C1477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Origin': domain,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': domain + '/xycx/queryCreditAction!qyxq_view.dhtml?reg_bus_ent_id=DCBB0FD56D324C87AD672F5D35EA3437&credit_ticket=AFD334549753B8FB11986D8C347561F2',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        url = domain + "/newChange/newChangeAction!getGj.dhtml"
        form_data = {
            "info_categ": "01",
            "reg_bus_ent_id": reg_bus_ent_id,
            "vchr_bmdm": "",
            "ent_name": "",
            "random": "%s" % random.random()
        }
        self._http_client.clear_cookies()
        response = self._verify_post(url, form_data, headers=headers)
        return response

    def get_xhxx_list(self, reg_bus_ent_id):
        # 协会信息
        headers = {
            'Accept': 'text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en-US;q=0.4,en;q=0.2',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # Cookie:CNZZDATA1257386840=621069940-1476929457-http%253A%252F%25%7C1477463362; JSESSIONID=YRnfYQhchW29GQGy5Kfp2VGxL1dNnbC1kz0ZjkHbn67BGms7MxJp!-1633019820
            'Host': host,
            'Origin': domain,
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            # 'Referer': domain + '/xycx/queryCreditAction!qyxq_view.dhtml?reg_bus_ent_id=DCBB0FD56D324C87AD672F5D35EA3437&credit_ticket=AFD334549753B8FB11986D8C347561F2',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        url = domain + "/newChange/newChangeAction!getGj.dhtml"
        form_data = {
            "info_categ": "06",
            "reg_bus_ent_id": reg_bus_ent_id,
            "vchr_bmdm": "",
            "ent_name": "",
            "random": "%s" % random.random()
        }
        self._http_client.clear_cookies()
        response = self._verify_post(url, form_data, headers=headers)
        return response
