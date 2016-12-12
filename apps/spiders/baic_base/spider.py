# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging
import time

from bs4 import BeautifulSoup
from ..common.proxy_server_pool.proxy_server_pool import ProxyServerPool

from apps.spiders.common.exception import MoreCheckverifyCodeTimesError, NeedrefreshProxyError, \
    NeedrefreshSearchKeyError
from apps.spiders.common.get_search_key import GetSearchKey
from captcha import read_body_to_string
from push_base import GongshangPush, ShuiwuPush, ZbPush, ZzjgdmPush, ShebaoPush
from site_client import SiteClient


class Spider(object):
    def __init__(self, config):
        self._config = config
        self.get_search_key = GetSearchKey(self._config.search_key_collection_name)
        self._proxy_server_pool = ProxyServerPool()
        self._proxy_server = None
        self._search_key = None
        pass

    def run(self):

        while True:
            self._search_key = self.get_search_key.get_search_key()
            if not self._search_key:
                self._proxy_server_pool.release_one(self._proxy_server)
                self._proxy_server = None
                logging.info("sleep 60*1....")
                time.sleep(60 * 1)
                continue

            try:
                self._refresh_proxy()
                self.proxy_search()
                self.get_search_key.remove_search_key(self._search_key)

            except Exception, e:
                logging.exception("_run->%s" % e)
                # raise e
                # continue

    def _refresh_proxy(self):
        if not self._proxy_server:
            self._proxy_server = self._proxy_server_pool.request_one()
        self._proxy_server.restart_adsl()
        time.sleep(1)
        self._proxy_ip, self._proxy_port = self._proxy_server.get_current_proxy()
        http_proxy = "http://%s:%s" % (self._proxy_ip, self._proxy_port)
        proxies = {"http": http_proxy}
        logging.info("++++++++proxies: %s++++++++++++" % proxies)
        self._client = SiteClient(self._config, proxies)
        pass

    def proxy_search(self):

        try:
            self.get_search()
        except Exception, e:
            logging.exception(e)
            self._refresh_proxy()

            self.proxy_search()
            # raise e
            pass

    def get_search(self):
        logging.info("get_search++++++++%s" % self._search_key)
        try:
            self._client.index_1()
        except Exception, e:
            logging.exception(e)
            raise NeedrefreshProxyError()

        check_code = self.get_verify_img_code()
        logging.info("check_code=%s" % check_code)
        check_code = self.check_verify_code(check_code)

        response = self._client.get_search_list(self._search_key, check_code)

        if response.content.find(u"您停留的时间过长") > -1:
            logging.debug("您停留的时间过长")
            raise NeedrefreshProxyError()
        if response.content.find(u"<title>Æµ·±·ÃÎÊ´íÎóÒ³Ãæ</title>") > -1:
            logging.debug("more time requests 您可能频繁重复请求")
            raise NeedrefreshProxyError()
        if response.content.find(u"提示：访问异常") > -1:
            logging.debug("<title>访问异常</title>")
            raise NeedrefreshSearchKeyError()
        if response.content.find(u"企业信用信息查询") > -1:
            self.parse_search_list(response)
        else:
            logging.debug(response.content)
            raise NeedrefreshProxyError()

    def get_verify_img_code(self, times=0):
        logging.info("get_verify_img_code.....")
        if times == 0:
            response = self._client.get_verify_img()
        else:
            response = self._client.refresh_verify_img()
        check_code = read_body_to_string(response.content)
        times += 1
        print "read verify code times: %s" % times
        if times >= 5:
            raise Exception("get more times verify code")
        if len(check_code) == 0:
            return self.get_verify_img_code(times)
        return check_code

    def check_verify_code(self, check_code, times=0):
        logging.info("check_verify_code.............")
        response = self._client.check_verify_code(check_code)
        logging.info("------response.content=%s-------" % response.content)
        if response.content == "true":
            return check_code
        else:
            times += 1
            if times >= 5:
                raise MoreCheckverifyCodeTimesError()
            check_code = self.get_verify_img_code(1)
            return self.check_verify_code(check_code, times)

    def parse_search_list(self, response):
        logging.info("parse_search_list..........")
        # logging.debug(response.content)
        # logging.debug(response.content.encode('gbk'))

        soup = BeautifulSoup(response.content, 'lxml')

        a_list = soup.select('table tr td font a')
        logging.info("+++++++++++++++++a_list len=%s+++++++++++++++++++" % len(a_list))
        for a in a_list:
            onclick = a["onclick"]
            reg_bus_ent_id = onclick.split('reg_bus_ent_id=')[1].split('&')[0]
            credit_ticket = onclick.split('credit_ticket=')[1].split('\'')[0]

            logging.info("++++++reg_bus_ent_id: %s++++++++++" % reg_bus_ent_id)
            logging.info("++++++credit_ticket: %s++++++++++" % credit_ticket)

            result = {}
            result.update({"reg_bus_ent_id": reg_bus_ent_id})

            self.get_company(reg_bus_ent_id, credit_ticket)

            # TODO set reg_bus_ent_id to other part to crawler

        try:
            page_count = soup.select_one('input[id="pagescount"]')['value']  # 总页数
            EntryPageNo = soup.select_one('input[id="EntryPageNo"]')['value']  # 当前页数
            # if EntryPageNo < page_count:
            #     EntryPageNo += 1
        except Exception, e:
            return
        self.next_page(int(EntryPageNo), int(page_count))

    def next_page(self, EntryPageNo, page_count):
        logging.info("next_page........%s/%s...." % (EntryPageNo, page_count))
        if EntryPageNo < page_count:
            pageNo = EntryPageNo + 1
            response = self._client.next_page(EntryPageNo, pageNo, self._search_key)
            self.parse_search_list(response)
        pass

    # -------------company detail----------------
    def get_company(self, reg_bus_ent_id, credit_ticket):
        logging.info("get_company.....%s........%s......" % (reg_bus_ent_id, credit_ticket))

        response = self._client.get_detail(reg_bus_ent_id, credit_ticket)
        # logging.debug(response.content)
        soup = BeautifulSoup(response.content, 'lxml')

        try:
            table_list = soup.select('div[class="jic"] table')
            company_name = None
            for i in range(1, len(table_list) / 2 + 1):
                f_lan_index = 2 * i - 2
                f_lan_table = table_list[f_lan_index]
                f_lbiao_table = table_list[f_lan_index + 1]
                text = f_lan_table.select_one('tr td').getText().strip()
                text = text.strip()

                if text == u"工商登记注册基本信息":
                    gsdjzc_info = self.parse_gsdjzc_info(f_lbiao_table)  # 工商登记注册基本信息
                    company_name = gsdjzc_info.get(u"名称")
                    GongshangPush().push_info(gsdjzc_info, company_name)
                    pass
                elif text == u"资本相关信息":
                    zbxg_info = self.parse_zbxg_info(f_lbiao_table)  # 资本相关信息
                    ZbPush().push_info(zbxg_info, company_name)
                    pass
                elif text == u"组织机构代码信息":
                    zzjgdm_info = self.parse_zzjgdm_info(f_lbiao_table)  # 组织机构代码信息
                    ZzjgdmPush().push_info(zzjgdm_info, company_name)
                    pass
                elif text == u"税务登记信息":
                    swdj_info = self.parse_swdj_info(f_lbiao_table)  # 税务登记信息
                    ShuiwuPush().push_info(swdj_info, company_name)
                    pass
                elif text == u"社保登记信息":
                    sbdj_info = self.parse_sbdj_info(f_lbiao_table)  # 社保登记信息
                    ShebaoPush().push_info(sbdj_info, company_name)
                    pass
                else:
                    logging.error("unknown text ->%s" % text)
                    exit(1)
        except Exception, e:
            logging.exception("parse_base_info->%s" % e)

    def parse_gsdjzc_info(self, f_lbiao_table):
        logging.info("parse_gsdjzc_info..............")
        # 解析工商登记注册基本信息
        gsdjzc_info = {}

        try:
            td_list = f_lbiao_table.select('tr td')

            for i in range(0, len(td_list) / 2):
                td_1 = td_list[i * 2]
                td_2 = td_list[i * 2 + 1]
                key = td_1.select_one('div').getText().replace(' ', '').replace('\n', '').replace('\t', '').replace('：',
                                                                                                                    '')
                value = td_2.getText().strip()
                try:
                    gsdjzc_info.update({key: value})
                except Exception, e:
                    logging.error("unknown key: %s" % key)
                    exit(1)

        except Exception, e:
            logging.exception("parse_gsdjzc_info->%s" % e)

        return gsdjzc_info

    def parse_zbxg_info(self, f_lbiao_table):
        logging.info("parse_zbxg_info..............")
        # 解析资本相关信息
        gsdjzc_info = {}
        try:
            td_list = f_lbiao_table.select('tr td')
            for i in range(0, len(td_list) / 2):
                td_1 = td_list[i * 2]
                td_2 = td_list[i * 2 + 1]
                try:
                    key = td_1.select_one('div').getText().strip()
                except Exception, e:
                    key = u"-"
                value = td_2.getText().strip()
                try:
                    gsdjzc_info.update({key: value})
                except Exception, e:
                    logging.error("unknown key: %s" % key)
                    exit(1)
        except Exception, e:
            logging.exception("parse_zbxg_info->%s" % e)

        return gsdjzc_info

    def parse_zzjgdm_info(self, f_lbiao_table):
        logging.info("parse_zzjgdm_info..............")
        # 解析组织机构代码信息
        zzjgdm_info = {}
        try:
            td_list = f_lbiao_table.select('tr td')
            for i in range(0, len(td_list) / 2):
                td_1 = td_list[i * 2]
                td_2 = td_list[i * 2 + 1]
                key = td_1.select_one('div').getText().strip()
                value = td_2.getText().strip()
                try:
                    zzjgdm_info.update({key: value})
                except Exception, e:
                    logging.error("unknown key: %s" % key)
                    exit(1)
        except Exception, e:
            logging.exception("parse_zzjgdm_info->%s" % e)

        return zzjgdm_info

    def parse_swdj_info(self, f_lbiao_table):
        logging.info("parse_swdj_info..............")
        # 解析税务登记信息
        gsdjzc_info = {}
        try:
            th_list = f_lbiao_table.select('tr th')
            td_list = f_lbiao_table.select('tr td')
            for i in range(0, len(th_list)):
                th_text = th_list[i].getText().strip().replace('：', '')
                td_text = td_list[i].getText().strip()
                gsdjzc_info.update({th_text: td_text})
        except Exception, e:
            logging.exception("parse_swdj_info->%s" % e)

        return gsdjzc_info

    def parse_sbdj_info(self, f_lbiao_table):
        logging.info("parse_sbdj_info..............")
        # 解析社保登记信息
        gsdjzc_info = {}
        try:
            th_list = f_lbiao_table.select('tr th')
            td_list = f_lbiao_table.select('tr td')
            for i in range(0, len(th_list)):
                th_text = th_list[i].getText().strip().replace('：', '')
                td_text = td_list[i].getText().strip()
                gsdjzc_info.update({th_text: td_text})
        except Exception, e:
            logging.exception("parse_sbdj_info->%s" % e)

        return gsdjzc_info
