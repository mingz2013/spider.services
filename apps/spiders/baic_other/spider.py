# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging

from bs4 import BeautifulSoup

from exception import NeedrefreshProxyError, HttpClientError, ErrorStatusCode
from get_proxy import GetProxy
from get_search_key import GetSearchKey
from mongo import QyxybaicLevel4DB
from site_client import SiteClient


# 其他信息->所有
class Spider(object):
    def __init__(self):
        self._client = None
        self._getProxy = GetProxy(4, 0)
        self._getSearchKey = GetSearchKey()
        pass

    def _refresh_proxy(self):

        self._proxy_ip, self._proxy_port, proxy_type = self._getProxy.get_proxy()
        http_proxy = "http://%s:%s" % (self._proxy_ip, self._proxy_port)
        proxies = {"http": http_proxy}
        logging.info("++++++++proxies: %s++++++++++++" % proxies)
        self._client = SiteClient(proxies)
        pass

    def run(self):
        try:
            # cur = QyxybaicDB.get_all()
            self._refresh_proxy()
            while True:
                try:
                    reg_bus_ent_id = self._getSearchKey.get_reg_bus_ent_id()
                    # reg_bus_ent_id = item['reg_bus_ent_id']
                    logging.info("-------------%s--------------" % reg_bus_ent_id)
                    if QyxybaicLevel4DB.get_one(reg_bus_ent_id):
                        logging.info("----------------is have-------------------")
                        continue

                    company = {"reg_bus_ent_id": reg_bus_ent_id}
                    company_info = self.get_company(reg_bus_ent_id)
                    company.update(company_info)
                    QyxybaicLevel4DB.upsert_company_detail_level_4(company)
                except NeedrefreshProxyError, err:
                    self._refresh_proxy()
                    continue
                except ErrorStatusCode, err:
                    self._refresh_proxy()
                    continue
                except HttpClientError, err:
                    self._refresh_proxy()
                    continue

        except Exception, e:
            logging.exception(e)
            pass

    def test(self, reg_bus_ent_id):
        logging.info("test...")
        company = self.get_company(reg_bus_ent_id)
        logging.info(company)

    # -------------company detail----------------
    def get_company(self, reg_bus_ent_id):
        logging.info("get_company.....%s............." % reg_bus_ent_id)

        company = {}
        # company.update({"base_info": self.parse_base_info(soup)})

        # company.update({"tzr_list": self.get_tzr_list(reg_bus_ent_id)})
        # company.update({"tzr_history_list": self.get_tzr_history_list(reg_bus_ent_id)})
        # company.update({"zyry_list": self.get_zyry_list(reg_bus_ent_id)})
        # company.update({"bgxx_list": self.get_bgxx_list(reg_bus_ent_id)})
        # company.update({"fzjg_list": self.get_fzjg_list(reg_bus_ent_id)})
        # company.update({"ztz_list": self.get_ztz_list(reg_bus_ent_id)})

        company.update({"other_info": self.get_other_info(reg_bus_ent_id)})
        # company.update({"gsgs_info": self.get_gsgs_info(reg_bus_ent_id)})

        return company

    # ++++++++其他信息++++++++++++++++++++++++++++ #
    def get_other_info(self, reg_bus_ent_id):
        # 其他信息
        other_info = {}
        other_info.update({"jsxx": self.get_jsxx_list(reg_bus_ent_id)})
        other_info.update({"tsxx": self.get_tsxx_list(reg_bus_ent_id)})
        other_info.update({"lhxx": self.get_lhxx_list(reg_bus_ent_id)})
        other_info.update({"xkzzxx": self.get_xkzzxx_list(reg_bus_ent_id)})
        other_info.update({"xhxx": self.get_xhxx_list(reg_bus_ent_id)})
        return other_info

    def get_jsxx_list(self, reg_bus_ent_id):
        # 警示信息
        response = self._client.get_jsxx_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        pass

    def get_tsxx_list(self, reg_bus_ent_id):
        # 提示信息
        response = self._client.get_tsxx_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        pass

    def get_lhxx_list(self, reg_bus_ent_id):
        # 良好信息
        response = self._client.get_lhxx_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        pass

    def get_xkzzxx_list(self, reg_bus_ent_id):
        # 许可资质信息
        response = self._client.get_xkzzxx_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        pass

    def get_xhxx_list(self, reg_bus_ent_id):
        # 协会信息
        response = self._client.get_xhxx_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        pass
