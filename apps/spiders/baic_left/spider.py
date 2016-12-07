# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging

from bs4 import BeautifulSoup

from apps.spiders.common.get_search_key import GetSearchKey
from site_client import SiteClient
from ..common.proxy_pool.proxy_pool import ProxyPool


class Spider(object):
    def __init__(self, config):
        self._config = config
        self.get_search_key = GetSearchKey(self._config.search_key_collection_name)
        self._proxy_pool = ProxyPool()
        self._search_key = None
        pass

    def run(self):

        while True:
            try:
                self._refresh_proxy()
                reg_bus_ent_id = self.get_search_key.get_reg_bus_ent_id()
                self.get_company(reg_bus_ent_id)
            except Exception, e:
                self._refresh_proxy()
                continue

    def _refresh_proxy(self):
        self._proxy_ip, self._proxy_port, proxy_type = self._proxy_pool.request_one()
        http_proxy = "http://%s:%s" % (self._proxy_ip, self._proxy_port)
        proxies = {"http": http_proxy}
        logging.info("++++++++proxies: %s++++++++++++" % proxies)
        self._client = SiteClient(self._config, proxies)
        pass

    # -------------company detail----------------
    def get_company(self, reg_bus_ent_id):
        logging.info("get_company.....%s............." % reg_bus_ent_id)

        company = {}
        # company.update({"base_info": self.parse_base_info(soup)})

        company.update({"tzr_list": self.get_tzr_list(reg_bus_ent_id)})
        company.update({"tzr_history_list": self.get_tzr_history_list(reg_bus_ent_id)})
        company.update({"zyry_list": self.get_zyry_list(reg_bus_ent_id)})
        # company.update({"bgxx_list": self.get_bgxx_list(reg_bus_ent_id)})  # TODO 变更信息,最后做,这个不好做
        company.update({"fzjg_list": self.get_fzjg_list(reg_bus_ent_id)})
        company.update({"ztz_list": self.get_ztz_list(reg_bus_ent_id)})

        # company.update({"other_info": self.get_other_info(reg_bus_ent_id)})
        # company.update({"gsgs_info": self.get_gsgs_info(reg_bus_ent_id)})

        return company

    # ---------------------left main------------------------
    def get_tzr_list(self, reg_bus_ent_id):
        logging.info("get_tzr_list..............")
        # 处理投资人信息
        tzr_list = []

        response = self._client.get_tzr_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        tr_list = soup.select('table[id="tableIdStyle"] > tr')
        tr_list = tr_list[1:-1]
        logging.debug("len : %s" % len(tr_list))
        for tr in tr_list:
            td_list = tr.select('td')
            if len(td_list) == 5:
                investor = {}
                investor.update({
                    "number": td_list[0].getText().strip(),  # 序号
                    "name": td_list[1].getText().strip(),  # 投资人名称
                    "investor_type": td_list[2].getText().strip(),  # 投资人类型
                    "card_type": td_list[3].getText().strip(),  # 证照类型
                    "card_number": td_list[4].getText().strip()  # 证照号码
                })
                tzr_list.append(investor)

        return tzr_list

    def get_tzr_history_list(self, reg_bus_ent_id):
        logging.info("get_tzr_history_list..............")
        # 处理投资人历史信息
        tzr_history_list = []

        response = self._client.get_tzr_history_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        tr_list = soup.select('table[id="tableIdStyle"] > tr')
        tr_list = tr_list[1:-1]
        logging.debug("len : %s" % len(tr_list))
        for tr in tr_list:
            td_list = tr.select('td')
            if len(td_list) == 9:
                investor = {}
                investor.update({
                    "number": td_list[0].getText().strip(),  # 序号
                    "name": td_list[1].getText().strip(),  # 投资人名称
                    "investor_type": td_list[2].getText().strip(),  # 投资人类型
                    "subscription_amount": td_list[3].getText().strip(),  # 认缴出资金额(万元)
                    "subscription_mode": td_list[4].getText().strip(),  # 认缴出资方式
                    "subscription_time": td_list[5].getText().strip(),  # 认缴出资时间
                    "paid_amount": td_list[6].getText().strip(),  # 实缴出资金额(万元)
                    "paid_mode": td_list[7].getText().strip(),  # 实缴出资方式
                    "paid_time": td_list[8].getText().strip(),  # 实缴出资时间
                })
                tzr_history_list.append(investor)

        return tzr_history_list

    def get_zyry_list(self, reg_bus_ent_id):
        logging.info("get_zyry_list..............")
        # 处理主要人员信息
        zyry_list = []

        response = self._client.get_zyry_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        tr_list = soup.select('table[id="tableIdStyle"] > tr')
        tr_list = tr_list[1:-1]
        logging.debug("len : %s" % len(tr_list))
        for tr in tr_list:
            td_list = tr.select('td')
            people = {}
            people.update({
                "number": td_list[0].getText().strip(),  # 序号
                "name": td_list[1].getText().strip(),  # 姓名
                "position": td_list[2].getText().strip(),  # 职位
                "sex": td_list[3].getText().strip(),  # 性别
            })
            zyry_list.append(people)

        return zyry_list

    def get_bgxx_list(self, reg_bus_ent_id):
        logging.info("get_bgxx_list..............")
        # 处理变更信息
        bgxx_list = []
        response = self._client.get_bgxx_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        tr_list = soup.select('table[id="tableIdStyle"] tr')
        tr_list = tr_list[1:-1]
        logging.debug("len : %s" % len(tr_list))
        for tr in tr_list:
            td_list = tr.select('td')
            change_info = {}
            change_info.update({
                "number": td_list[0].getText().strip(),  # 序号
                "time": td_list[1].getText().strip(),  # 变更时间
                "field": td_list[2].getText().strip(),  # 变更项
                # "change_before": td_list[3].getText(), # 变更前    # TODO 这里还有子页, 后面在搞
                # "change_after": td_list[4].getText(),  # 变更后
            })

            bgxx_list.append(change_info)
        return bgxx_list

    def get_fzjg_list(self, reg_bus_ent_id):
        logging.info("get_fzjg_list..............")
        # 分支机构
        fzjg_list = []
        response = self._client.get_fzjg_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        tr_list = soup.select('table[id="tableIdStyle"] tr')
        tr_list = tr_list[1:-1]
        if len(tr_list) > 0:
            logging.debug("fenzhijigou > 0")
            exit(-1)
        for tr in tr_list:
            td_list = tr.select('td')
            fzjg_info = {}
            # TODO 解析
            # fzjg_info.update({
            #     "number": td_list[0].getText().strip(),  # 序号
            #     "company_name": td_list[1].getText().strip(),  # 主体名称
            #     "zch": td_list[2].getText().strip(),  # 注册号
            #     "fddbr": td_list[3].getText().strip(), # 法定代表人
            #     "address": td_list[3].getText().strip(),  # 地址
            # })

            fzjg_list.append(fzjg_info)
        return fzjg_list

    def get_ztz_list(self, reg_bus_ent_id):
        logging.info("get_ztz_list..............")
        # 再投资信息
        ztz_list = []
        response = self._client.get_ztzxx_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        tr_list = soup.select('table[id="tableIdStyle"] tr')
        tr_list = tr_list[1:-1]
        logging.debug("len : %s" % len(tr_list))
        for tr in tr_list:
            td_list = tr.select('td')
            ztz_info = {}
            ztz_info.update({
                "number": td_list[0].getText().strip(),  # 序号
                "company_name": td_list[1].getText().strip(),  # 主体名称
                "zch": td_list[2].getText().strip(),  # 注册号
                "fddbr": td_list[3].getText().strip(),  # 法定代表人
                "address": td_list[3].getText().strip(),  # 地址
            })

            ztz_list.append(ztz_info)
        return ztz_list
