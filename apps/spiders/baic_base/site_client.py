# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging
import math

# import time
# import urllib2

from bs4 import BeautifulSoup

import random

from ..common.base_site_client import BaseSiteClient


class SiteClient(BaseSiteClient):
    def __init__(self, config, proxies):
        BaseSiteClient.__init__(config, proxies)

        self.credit_ticket = None
        self.currentTimeMillis = None
        self._detail_url = None
        self._index_1_url = None
        self._index_2_url = None
        self._search_list_url = None
        pass

    def index_1(self):
        index_1_url = self._config.domain + "/"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': '',
            'Host': self._config.host,
            'Pragma': 'no-cache',
            # 'Referer': 'http://www.chinabidding.com/',
            'Upgrade-Insecure-Requests': '1',
        }

        response = self._verify_get(index_1_url, headers=headers)
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
            'Host': self._config.host,
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
        url = self._config.domain + "/CheckCodeYunSuan?currentTimeMillis=%s" % self.currentTimeMillis
        headers = {
            'Accept': 'image/webp,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': '',
            'Host': self._config.host,
            'Pragma': 'no-cache',
            'Referer': self._index_2_url,
        }
        response = self._verify_get(url, headers=headers)
        return response

    def refresh_verify_img(self):
        url = self._config.domain + "/CheckCodeYunSuan?currentTimeMillis=%s&r=%s" % (
            self.currentTimeMillis, random.random())
        headers = {
            'Accept': 'image/webp,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': '',
            'Host': self._config.host,
            'Pragma': 'no-cache',
            'Referer': self._index_2_url,
        }
        response = self._verify_get(url, headers=headers)
        return response

    def check_verify_code(self, check_code):
        url = self._config.domain + "/login/loginAction!checkCode.dhtml?check_code=%s&currentTimeMillis=%s&random=%s" % (
            check_code, self.currentTimeMillis, math.ceil(random.random() * 100000))
        headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            # 'Cookie': '',
            'Host': self._config.host,
            'Origin': self._config.domain,
            'Pragma': 'no-cache',
            'Referer': self._index_2_url,
            'X-Requested-With': 'XMLHttpRequest'
        }
        logging.info("check_verify_code url:->%s" % url)
        response = self._verify_post(url, headers=headers)
        return response

    def get_search_list(self, search_key, check_code):
        url = self._config.domain + "/lucene/luceneAction!NetCreditLucene.dhtml?currentTimeMillis=%s&credit_ticket=%s&check_code=%s" % (
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
            'Host': self._config.host,
            'Origin': self._config.domain,
            'Pragma': 'no-cache',
            'Referer': self._index_2_url,
            'Upgrade-Insecure-Requests': '1',
        }
        response = self._verify_post(url, form_data, headers=headers)
        self._search_list_url = url
        return response

    def next_page(self, EntryPageNo, pageNo, search_key):
        url = self._config.domain + "/lucene/luceneAction!NetCreditLucene.dhtml?currentTimeMillis=%s&credit_ticket=%s" % (
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
            'Host': self._config.host,
            'Origin': self._config.domain,
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
        url = self._config.domain + "/xycx/queryCreditAction!qyxq_view.dhtml?reg_bus_ent_id=%s&credit_ticket=%s" % (
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
            'Host': self._config.host,
            # 'Origin': self._config.domain,
            'Pragma': 'no-cache',
            'Referer': self._search_list_url,
            'Upgrade-Insecure-Requests': '1',
        }
        response = self._verify_get(url, headers=headers)
        self._detail_url = url
        return response
