# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging
import math

# import time
# import urllib2

from bs4 import BeautifulSoup

from http_client import HTTPClient

from exception import Error302, Error403, Error404, Error502, Error503, ErrorStatusCode, HttpClientError
from config import default_headers, USER_AGENTS
import random
from config import host, domain, download_timeout


class SiteClient(object):
    def __init__(self, proxies):
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
        pass

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
                raise Error302()
            elif response.status_code == 403:
                raise Error403()
            elif response.status_code == 404:
                raise Error404()
            elif response.status_code == 502:
                raise Error502()
            elif response.status_code == 503:
                raise Error503()
            else:
                raise ErrorStatusCode(response.status_code)
            return response
        except Error403, err:
            raise err
        except HttpClientError, err:
            times += 1
            if times < 2:
                return self._verify_post(url, data=data, json=json, times=times, headers=headers, timeout=timeout)
            else:
                raise err

    def _verify_get(self, url, times=0, headers=default_headers, refresh_ip=False, timeout=download_timeout):
        headers.update({
            'User-Agent': self._user_agent,
            # "Proxy-Authorization": self.get_authHeader(refresh_ip)
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
            return response
        except Error403, err:
            raise err
        except HttpClientError, err:
            times += 1
            if times < 2:
                return self._verify_get(url, times=times, headers=headers, refresh_ip=refresh_ip, timeout=timeout)
            else:
                raise err

    # def get_authHeader(self, refresh_ip=False):
    #
    #     # 请替换appkey和secret
    #     appkey = "17644285"
    #     secret = "54d9b18269c54a19a841cc25f4633cac"
    #
    #     paramMap = {
    #         "app_key": appkey,
    #         "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),  # 如果你的程序在国外，请进行时区处理
    #         "with-transaction": 1,
    #         # "enable-simulate": False,
    #     }
    #
    #     if refresh_ip:
    #         paramMap.update({
    #             "release-transaction": "1"
    #         })
    #
    #     # 排序
    #     keys = paramMap.keys()
    #     keys.sort()
    #
    #     codes = "%s%s%s" % (secret, str().join('%s%s' % (key, paramMap[key]) for key in keys), secret)
    #
    #     # 计算签名
    #     sign = hashlib.md5(codes).hexdigest().upper()
    #
    #     paramMap["sign"] = sign
    #
    #     # 拼装请求头Proxy-Authorization的值
    #     keys = paramMap.keys()
    #     authHeader = "MYH-AUTH-MD5 " + str('&').join('%s=%s' % (key, paramMap[key]) for key in keys)
    #
    #     print "authHeader", authHeader
    #     return authHeader

    def index_1(self):
        index_1_url = domain + "/"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': '',
            'Host': host,
            'Pragma': 'no-cache',
            # 'Referer': 'http://www.chinabidding.com/',
            'Upgrade-Insecure-Requests': '1',
        }

        response = self._verify_get(index_1_url, headers=headers, refresh_ip=True)
        self._index_1_url = index_1_url
        # logging.debug(response.content)
        soup = BeautifulSoup(response.content, 'lxml')
        index_2_url = soup.select_one('frame')['src']
        logging.info("index_2_url:-> %s" % index_2_url)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': '',
            'Host': host,
            'Pragma': 'no-cache',
            'Referer': self._index_1_url,
            'Upgrade-Insecure-Requests': '1'
        }
        response = self._verify_get(index_2_url, headers=headers)
        self._index_2_url = index_2_url
        # soup = BeautifulSoup(response.content, 'lxml')
        self.credit_ticket = None
        # credit_ticket
        txt = response.content
        # print txt.split('\n')
        for line in txt.split('\n'):
            # print "line: %s" % line
            if line.find('var credit_ticket') > -1:
                # print "line: %s" % line
                self.credit_ticket = line.split('"')[1]
                logging.info("------credit_ticket: %s--------" % self.credit_ticket)
                break

        soup = BeautifulSoup(response.content, 'lxml')
        self.currentTimeMillis = soup.select_one('input[id="currentTimeMillis"]')['value']
        logging.info("-----currentTimeMillis:->%s------" % self.currentTimeMillis)

    def get_verify_img(self):
        url = domain + "/CheckCodeYunSuan?currentTimeMillis=%s" % self.currentTimeMillis
        headers = {
            'Accept': 'image/webp,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': '',
            'Host': host,
            'Pragma': 'no-cache',
            'Referer': self._index_2_url,
        }
        response = self._verify_get(url, headers=headers)
        return response

    def refresh_verify_img(self):
        url = domain + "/CheckCodeYunSuan?currentTimeMillis=%s&r=%s" % (
            self.currentTimeMillis, random.random())
        headers = {
            'Accept': 'image/webp,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': '',
            'Host': host,
            'Pragma': 'no-cache',
            'Referer': self._index_2_url,
        }
        response = self._verify_get(url, headers=headers)
        return response

    def check_verify_code(self, check_code):
        url = domain + "/login/loginAction!checkCode.dhtml?check_code=%s&currentTimeMillis=%s&random=%s" % (
            check_code, self.currentTimeMillis, math.ceil(random.random() * 100000))
        headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            # 'Cookie': '',
            'Host': host,
            'Origin': domain,
            'Pragma': 'no-cache',
            'Referer': self._index_2_url,
            'X-Requested-With': 'XMLHttpRequest'
        }
        logging.info("check_verify_code url:->%s" % url)
        response = self._verify_post(url, headers=headers)
        return response

    def get_search_list(self, search_key, check_code):
        url = domain + "/lucene/luceneAction!NetCreditLucene.dhtml?currentTimeMillis=%s&credit_ticket=%s&check_code=%s" % (
            self.currentTimeMillis, self.credit_ticket, check_code)
        form_data = {
            "queryStr": "%s" % search_key,
            "module": "",
            "idFlag": "qyxy"
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Content-Length': '47',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': '',
            'Host': host,
            'Origin': domain,
            'Pragma': 'no-cache',
            'Referer': self._index_2_url,
            'Upgrade-Insecure-Requests': '1',
        }
        response = self._verify_post(url, form_data, headers=headers)
        self._search_list_url = url
        return response

    def next_page(self, EntryPageNo, pageNo, search_key):
        url = domain + "/lucene/luceneAction!NetCreditLucene.dhtml?currentTimeMillis=%s&credit_ticket=%s" % (
            self.currentTimeMillis, self.credit_ticket)
        form_data = {
            "queryStr": "%s" % search_key,
            "module": "",
            "idFlag": "qyxy",
            "SelectPageSize": "10",
            "EntryPageNo": "%s" % EntryPageNo,
            "pageNo": "%s" % pageNo,
            "pageSize": "10",
            "clear": "",
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Content-Length': '47',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': '',
            'Host': host,
            'Origin': domain,
            'Pragma': 'no-cache',
            'Referer': self._search_list_url,
            'Upgrade-Insecure-Requests': '1',
        }
        response = self._verify_post(url, form_data, headers=headers)
        self._search_list_url = url
        return response

    # -------------right main----------------------------
    def get_detail(self, reg_bus_ent_id, credit_ticket):
        # 公司详情页面
        url = domain + "/xycx/queryCreditAction!qyxq_view.dhtml?reg_bus_ent_id=%s&credit_ticket=%s" % (
            reg_bus_ent_id, credit_ticket)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Content-Length': '47',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': '',
            'Host': host,
            # 'Origin': '',
            'Pragma': 'no-cache',
            'Referer': self._search_list_url,
            'Upgrade-Insecure-Requests': '1',
        }
        response = self._verify_get(url, headers=headers)
        self._detail_url = url
        return response

        # # -----------left main-----------------------------
        # def get_tzr_list(self, reg_bus_ent_id):
        #     # 投资人
        #     url = domain + "/xycx/queryCreditAction!tzrlist_all.dhtml?reg_bus_ent_id=%s&ent_page=1&clear=true&newInv=newInv&fqr=" % reg_bus_ent_id
        #     response = self._verify_get(url)
        #     return response
        #
        # def get_tzr_history_list(self, reg_bus_ent_id):
        #     # 投资人历史
        #     url = domain + "/xycx/queryCreditAction!tzrlist_hs_all.dhtml?reg_bus_ent_id=%s&ent_page=1&clear=true&fqr=" % reg_bus_ent_id
        #     response = self._verify_get(url)
        #     return response
        #
        # def get_zyry_list(self, reg_bus_ent_id):
        #     # 重要人员
        #     url = domain + "/xycx/queryCreditAction!queryTzrxx_all.dhtml?reg_bus_ent_id=%s&clear=true" % reg_bus_ent_id
        #     response = self._verify_get(url)
        #     return response
        #
        # def get_bgxx_list(self, reg_bus_ent_id):
        #     # 变更信息
        #     url = domain + "/newChange/newChangeAction!bgxx_view.dhtml?reg_bus_ent_id=%s" % reg_bus_ent_id
        #     response = self._verify_get(url)
        #     return response
        #
        # def get_fzjg_list(self, reg_bus_ent_id):
        #     # 分支机构
        #     url = domain + "/xycx/queryCreditAction!getEnt_Fzjgxx.dhtml?reg_bus_ent_id=%s&clear=true" % reg_bus_ent_id
        #     response = self._verify_get(url)
        #     return response
        #
        # def get_ztzxx_list(self, reg_bus_ent_id):
        #     # 再投资信息
        #     url = domain + "/xycx/queryCreditAction!getEnt_Ztzxx.dhtml?reg_bus_ent_id=%s&clear=true&moreInfo=moreInfo" % reg_bus_ent_id
        #     response = self._verify_get(url)
        #     return response
        #
        # # -------------其他信息------------------------------------
        # def get_jsxx_list(self, reg_bus_ent_id):
        #     # 警示信息
        #     url = domain + "/newChange/newChangeAction!getGj.dhtml"
        #     form_data = {
        #         "info_categ": "04",
        #         "reg_bus_ent_id": reg_bus_ent_id,
        #         "vchr_bmdm": "",
        #         "ent_name": "",
        #         "random": "%s" % random.random()
        #     }
        #     response = self._verify_post(url, form_data)
        #     return response
        #
        # def get_tsxx_list(self, reg_bus_ent_id):
        #     # 提示信息
        #     url = domain + "/newChange/newChangeAction!getGj.dhtml"
        #     form_data = {
        #         "info_categ": "03",
        #         "reg_bus_ent_id": reg_bus_ent_id,
        #         "vchr_bmdm": "",
        #         "ent_name": "",
        #         "random": "%s" % random.random()
        #     }
        #     response = self._verify_post(url, form_data)
        #     return response
        #
        # def get_lhxx_list(self, reg_bus_ent_id):
        #     # 良好信息
        #     url = domain + "/newChange/newChangeAction!getGj.dhtml"
        #     form_data = {
        #         "info_categ": "02",
        #         "reg_bus_ent_id": reg_bus_ent_id,
        #         "vchr_bmdm": "",
        #         "ent_name": "",
        #         "random": "%s" % random.random()
        #     }
        #     response = self._verify_post(url, form_data)
        #     return response
        #
        # def get_xkzzxx_list(self, reg_bus_ent_id):
        #     # 许可资质信息
        #     url = domain + "/newChange/newChangeAction!getGj.dhtml"
        #     form_data = {
        #         "info_categ": "01",
        #         "reg_bus_ent_id": reg_bus_ent_id,
        #         "vchr_bmdm": "",
        #         "ent_name": "",
        #         "random": "%s" % random.random()
        #     }
        #     response = self._verify_post(url, form_data)
        #     return response
        #
        # def get_xhxx_list(self, reg_bus_ent_id):
        #     # 协会信息
        #     url = domain + "/newChange/newChangeAction!getGj.dhtml"
        #     form_data = {
        #         "info_categ": "06",
        #         "reg_bus_ent_id": reg_bus_ent_id,
        #         "vchr_bmdm": "",
        #         "ent_name": "",
        #         "random": "%s" % random.random()
        #     }
        #     response = self._verify_post(url, form_data)
        #     return response
        #
        # # -------------公司公示信息----------------------------------------
        # def get_qynb_list(self, reg_bus_ent_id):
        #     # 企业年报
        #     url = domain + "/entPub/entPubAction!getTabForNB_new.dhtml?entId=%s&flag_num=0&clear=true&timeStamp=%s" % (
        #         reg_bus_ent_id, get_timeStamp())
        #     response = self._verify_get(url)
        #     return response
        #
        # def get_gdcz_list(self, reg_bus_ent_id):
        #     # 股东出资
        #     url = domain + "/newChange/newChangeAction!getTabForNB_new.dhtml?entId=%s&flag_num=1&clear=true&timeStamp=%s" % (
        #         reg_bus_ent_id, get_timeStamp())
        #     response = self._verify_get(url)
        #     return response
        #
        # def get_gqbg_list(self, reg_bus_ent_id):
        #     # 股权变更信息
        #     url = domain + "/newChange/newChangeAction!getTabForNB_new.dhtml?entId=%s&flag_num=2&clear=true&timeStamp=%s" % (
        #         reg_bus_ent_id, get_timeStamp())
        #     response = self._verify_get(url)
        #     return response
        #
        # def get_xzxk_list(self, reg_bus_ent_id):
        #     # 行政许可
        #     url = domain + "/newChange/newChangeAction!getTabForNB_new.dhtml?entId=%s&flag_num=3&clear=true&timeStamp=%s" % (
        #         reg_bus_ent_id, get_timeStamp())
        #     response = self._verify_get(url)
        #     return response
        #
        # def get_zscq_list(self, reg_bus_ent_id):
        #     # 知识产权
        #     url = domain + "/newChange/newChangeAction!getTabForNB_new.dhtml?entId=%s&flag_num=4&clear=true&timeStamp=%s" % (
        #         reg_bus_ent_id, get_timeStamp())
        #     response = self._verify_get(url)
        #     return response
        #
        # def get_xzcf_list(self, reg_bus_ent_id):
        #     # 行政处罚
        #     url = domain + "/newChange/newChangeAction!getTabForNB_new.dhtml?entId=%s&flag_num=5&clear=true&timeStamp=%s" % (
        #         reg_bus_ent_id, get_timeStamp())
        #     response = self._verify_get(url)
        #     return response
