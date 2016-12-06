# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging

from bs4 import BeautifulSoup

from captcha import read_body_to_string
from apps.spiders.common.exception import Error302, Error403, Error404, Error502, Error503, ErrorStatusCode, \
    HttpClientError, \
    MoreCheckverifyCodeTimesError, NeedrefreshProxyError, NeedrefreshSearchKeyError
from mongo import QyxybaicDB
from mredis import RedisClient
from site_client import SiteClient
# from utils import get_1000_txt
from get_proxy import GetProxy


# from get_search_key import GetSearchKey


# from config import proxies

class Spider(object):
    def __init__(self, thread_id=0):
        # self._txt = get_1000_txt()

        self._getProxy = GetProxy(0, thread_id)
        # self._client = SiteClient(proxies)
        # self._getSearchKey = GetSearchKey()
        # self._proxy_ip = None
        # self._proxy_port = None
        self._search_key = None
        # self.thread_id = thread_id
        pass

    def run(self, type):
        logging.info("+++++++++++++run++++++++++++++++")
        try:
            if type == 1:
                # self._run()
                pass
            elif type == 2:
                self._run_2()
            else:
                raise Exception("error run type")
            logging.info("++++++++++++++success finish!!!++++++++")
        except Exception, e:
            logging.exception(e.message)
            pass

    # def _run(self):
    #
    #     for i in range(0, len(self._txt)):
    #         # if i % 2 == 0:
    #         for j in range(i, len(self._txt)):
    #             # j = i + 1
    #             logging.info("(i, j):->(%s, %s)" % (i, j))
    #             self._search_key = self._txt[i] + self._txt[j]
    #             if RedisClient.get_search_key(self._search_key):
    #                 continue
    #             try:
    #                 self._refresh_proxy(remove_current=False)
    #                 self.proxy_search()
    #                 RedisClient.set_search_key(self._search_key)
    #             except Exception, e:
    #                 logging.exception("_run->%s" % e)
    #                 raise e
    #                 # continue

    def _run_2(self):
        self._refresh_proxy(remove_current=False)
        while True:

            try:
                self._refresh_search_key()
                # search_key = item['company_name']
                logging.info("+++++++ search_key -> %s++++++++++" % self._search_key)
                # if RedisClient.get_search_key(self._search_key):
                #     continue
                if QyxybaicDB.check_have(self._search_key):
                    logging.info("-----------------pass-------------------")
                    QyxybaicDB.remove_search_key_from_need(self._search_key)
                    continue
                # self._refresh_proxy(remove_current=True)
                self.proxy_search()
                # self.get_search()
                # RedisClient.set_search_key(self._search_key)
                QyxybaicDB.upsert_search_key_have(self._search_key)
                QyxybaicDB.remove_search_key_from_need(self._search_key)

            except Exception, e:
                logging.exception("_run->%s" % e)
                raise e
                # continue

    def _refresh_proxy(self, remove_current=True):
        # if remove_current:
        #     self._getProxy.remove_proxy(self._proxy_ip, self._proxy_port)
        self._proxy_ip, self._proxy_port, proxy_type = self._getProxy.get_proxy()
        http_proxy = "http://%s:%s" % (self._proxy_ip, self._proxy_port)
        proxies = {"http": http_proxy}
        logging.info("++++++++proxies: %s++++++++++++" % proxies)
        self._client = SiteClient(proxies)
        pass

    def _refresh_search_key(self):
        # self._search_key = self._getSearchKey.get_search_key()
        item = QyxybaicDB.get_random_one_search_key_need()
        self._search_key = item['search_key']
        pass

    def proxy_search(self):

        try:
            self.get_search()
        except Error302, err:
            logging.error(err.message)
            self._refresh_search_key()
            self._refresh_proxy()
            self.proxy_search()
        except Error403, err:
            logging.error(err.message)
            self._refresh_search_key()
            self._refresh_proxy()
            self.proxy_search()
        except Error404, err:
            logging.error(err.message)
            self._refresh_search_key()
            self._refresh_proxy()
            self.proxy_search()
        except Error502, err:
            logging.error(err.message)
            self._refresh_search_key()
            self._refresh_proxy()
            self.proxy_search()
        except Error503, err:
            logging.error(err.message)
            self._refresh_search_key()
            self._refresh_proxy()
            self.proxy_search()
        except ErrorStatusCode, err:
            logging.error(err.message)
            self._refresh_search_key()
            self._refresh_proxy()
            self.proxy_search()
        except HttpClientError, err:
            logging.error(err.message)
            self._refresh_search_key()
            self._refresh_proxy()
            self.proxy_search()
        except MoreCheckverifyCodeTimesError, err:
            logging.error(err.message)
            self._refresh_search_key()
            self._refresh_proxy()
            self.proxy_search()
        except NeedrefreshProxyError, err:
            logging.error(err.message)
            # self._getProxy.remove_proxy(err._proxy_ip, err._proxy_port)
            self._refresh_search_key()
            self._refresh_proxy()
            self.proxy_search()
        except NeedrefreshSearchKeyError, err:
            logging.error(err.message)
            self._refresh_search_key()
            self.proxy_search()
        except Exception, e:
            logging.exception(e)
            self._refresh_proxy()
            self._refresh_search_key()
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

            if RedisClient.get_reg_bug_ent_id(reg_bus_ent_id):
                logging.info("+++++++++++++pass+++++++++")
                continue

            result = {}
            result.update({"reg_bus_ent_id": reg_bus_ent_id})

            company = self.get_company(reg_bus_ent_id, credit_ticket)

            result.update(company)

            QyxybaicDB.upsert_company(result)

            RedisClient.set_reg_bug_ent_id(reg_bus_ent_id)
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

        company = {}
        company.update({"base_info": self.parse_base_info(soup)})

        # company.update({"tzr_list": self.get_tzr_list(reg_bus_ent_id)})
        # company.update({"tzr_history_list": self.get_tzr_history_list(reg_bus_ent_id)})
        # company.update({"zyry_list": self.get_zyry_list(reg_bus_ent_id)})
        # company.update({"bgxx_list": self.get_bgxx_list(reg_bus_ent_id)})
        # company.update({"fzjg_list": self.get_fzjg_list(reg_bus_ent_id)})
        # company.update({"ztz_list": self.get_ztz_list(reg_bus_ent_id)})

        # company.update({"other_info": self.get_other_info(reg_bus_ent_id)})
        # company.update({"gsgs_info": self.get_gsgs_info(reg_bus_ent_id)})

        return company

    # # ---------------------left main------------------------
    # def get_tzr_list(self, reg_bus_ent_id):
    #     logging.info("get_tzr_list..............")
    #     # 处理投资人信息
    #     tzr_list = []
    #
    #     response = self._client.get_tzr_list(reg_bus_ent_id)
    #     soup = BeautifulSoup(response.content, 'lxml')
    #     tr_list = soup.select('table[id="tableIdStyle"] tr')
    #     tr_list = tr_list[1:-1]
    #     for tr in tr_list:
    #         td_list = tr.select('td')
    #         if len(td_list) == 5:
    #             investor = {}
    #             investor.update({
    #                 "number": td_list[0].getText(),  # 序号
    #                 "name": td_list[1].getText(),  # 投资人名称
    #                 "investor_type": td_list[2].getText(),  # 投资人类型
    #                 "card_type": td_list[3].getText(),  # 证照类型
    #                 "card_number": td_list[4].getText()  # 证照号码
    #             })
    #             tzr_list.append(investor)
    #
    #     return tzr_list
    #
    # def get_tzr_history_list(self, reg_bus_ent_id):
    #     logging.info("get_tzr_history_list..............")
    #     # 处理投资人历史信息
    #     tzr_history_list = []
    #
    #     response = self._client.get_tzr_history_list(reg_bus_ent_id)
    #     soup = BeautifulSoup(response.content, 'lxml')
    #     tr_list = soup.select('table[id="tableIdStyle"] tr')
    #     tr_list = tr_list[1:-1]
    #     for tr in tr_list:
    #         td_list = tr.select('td')
    #         if len(td_list) == 9:
    #             investor = {}
    #             investor.update({
    #                 "number": td_list[0].getText(),  # 序号
    #                 "name": td_list[1].getText(),  # 投资人名称
    #                 "investor_type": td_list[2].getText(),  # 投资人类型
    #                 "subscription_amount": td_list[3].getText(),  # 认缴出资金额(万元)
    #                 "subscription_mode": td_list[4].getText(),  # 认缴出资方式
    #                 "subscription_time": td_list[5].getText(),  # 认缴出资时间
    #                 "paid_amount": td_list[6].getText(),  # 实缴出资金额(万元)
    #                 "paid_mode": td_list[7].getText(),  # 实缴出资方式
    #                 "paid_time": td_list[8].getText(),  # 实缴出资时间
    #             })
    #             tzr_history_list.append(investor)
    #
    #     return tzr_history_list
    #
    # def get_zyry_list(self, reg_bus_ent_id):
    #     logging.info("get_zyry_list..............")
    #     # 处理主要人员信息
    #     zyry_list = []
    #
    #     response = self._client.get_zyry_list(reg_bus_ent_id)
    #     soup = BeautifulSoup(response.content, 'lxml')
    #     tr_list = soup.select('table[id="tableIdStyle"] tr')
    #     tr_list = tr_list[1:-1]
    #     for tr in tr_list:
    #         td_list = tr.select('td')
    #         people = {}
    #         people.update({
    #             "number": td_list[0].getText(),  # 序号
    #             "name": td_list[1].getText(),  # 姓名
    #             "position": td_list[2].getText(),  # 职位
    #             "sex": td_list[3].getText(),  # 性别
    #
    #         })
    #         zyry_list.append(people)
    #
    #     return zyry_list
    #
    # def get_bgxx_list(self, reg_bus_ent_id):
    #     logging.info("get_bgxx_list..............")
    #     # 处理变更信息
    #     bgxx_list = []
    #     response = self._client.get_bgxx_list(reg_bus_ent_id)
    #     soup = BeautifulSoup(response.content, 'lxml')
    #     return bgxx_list
    #
    # def get_fzjg_list(self, reg_bus_ent_id):
    #     # 分支机构
    #     fzjg_list = []
    #     response = self._client.get_fzjg_list(reg_bus_ent_id)
    #     soup = BeautifulSoup(response.content, 'lxml')
    #     return fzjg_list
    #
    # def get_ztz_list(self, reg_bus_ent_id):
    #     # 再投资信息
    #     ztz_list = []
    #     response = self._client.get_ztzxx_list(reg_bus_ent_id)
    #     soup = BeautifulSoup(response.content, 'lxml')
    #
    #     return ztz_list

    # ------------right main-------------------------#
    # ++++++++基本信息++++++++++++++++++++++++++++++ #
    def parse_base_info(self, soup):
        logging.info("parse_base_info..............")
        #  基础信息
        base_info = {}

        try:
            table_list = soup.select('div[class="jic"] table')
            for i in range(1, len(table_list) / 2 + 1):
                f_lan_index = 2 * i - 2
                f_lan_table = table_list[f_lan_index]
                f_lbiao_table = table_list[f_lan_index + 1]
                text = f_lan_table.select_one('tr td').getText().strip()
                text = text.strip()

                if text == u"工商登记注册基本信息":
                    base_info.update({"gsdjzc_info": self.parse_gsdjzc_info(f_lbiao_table)})  # 工商登记注册基本信息
                    pass
                elif text == u"资本相关信息":
                    base_info.update({"zbxg_info": self.parse_zbxg_info(f_lbiao_table)})  # 资本相关信息
                    pass
                elif text == u"组织机构代码信息":
                    base_info.update({"zzjgdm_info": self.parse_zzjgdm_info(f_lbiao_table)})  # 组织机构代码信息
                    pass
                elif text == u"税务登记信息":
                    base_info.update({"swdj_info": self.parse_swdj_info(f_lbiao_table)})  # 税务登记信息
                    pass
                elif text == u"社保登记信息":
                    base_info.update({"sbdj_info": self.parse_sbdj_info(f_lbiao_table)})  # 社保登记信息
                    pass
                else:
                    logging.error("unknown text ->%s" % text)
                    exit(1)
        except Exception, e:
            logging.exception("parse_base_info->%s" % e)

        return base_info

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

        # # ++++++++其他信息++++++++++++++++++++++++++++ #
        # def get_other_info(self, reg_bus_ent_id):
        #     other_info = {}
        #     other_info.update({"jsxx": self.get_jsxx_list(reg_bus_ent_id)})
        #     other_info.update({"tsxx": self.get_tsxx_list(reg_bus_ent_id)})
        #     other_info.update({"lhxx": self.get_lhxx_list(reg_bus_ent_id)})
        #     other_info.update({"xkzzxx": self.get_xkzzxx_list(reg_bus_ent_id)})
        #     other_info.update({"xhxx": self.get_xhxx_list(reg_bus_ent_id)})
        #     return other_info
        #
        # def get_jsxx_list(self, reg_bus_ent_id):
        #     response = self._client.get_jsxx_list(reg_bus_ent_id)
        #     soup = BeautifulSoup(response.content, 'lxml')
        #     pass
        #
        # def get_tsxx_list(self, reg_bus_ent_id):
        #     response = self._client.get_tsxx_list(reg_bus_ent_id)
        #     soup = BeautifulSoup(response.content, 'lxml')
        #     pass
        #
        # def get_lhxx_list(self, reg_bus_ent_id):
        #     response = self._client.get_lhxx_list(reg_bus_ent_id)
        #     soup = BeautifulSoup(response.content, 'lxml')
        #     pass
        #
        # def get_xkzzxx_list(self, reg_bus_ent_id):
        #     response = self._client.get_xkzzxx_list(reg_bus_ent_id)
        #     soup = BeautifulSoup(response.content, 'lxml')
        #     pass
        #
        # def get_xhxx_list(self, reg_bus_ent_id):
        #     response = self._client.get_xhxx_list(reg_bus_ent_id)
        #     soup = BeautifulSoup(response.content, 'lxml')
        #     pass
        #
        # # ++++++++公司公示信息+++++++++++++++++++++++++ #
        # def get_gsgs_info(self, reg_bus_ent_id):
        #     gsgs_info = {}
        #     gsgs_info.update({"qynb": self.get_qynb_list(reg_bus_ent_id)})
        #     gsgs_info.update({"gdcz": self.get_gdcz_list(reg_bus_ent_id)})
        #     gsgs_info.update({"gqbg": self.get_gqbg_list(reg_bus_ent_id)})
        #     gsgs_info.update({"xzxk": self.get_xzxk_list(reg_bus_ent_id)})
        #     gsgs_info.update({"zscq": self.get_zscq_list(reg_bus_ent_id)})
        #     gsgs_info.update({"xzcf": self.get_xzcf_list(reg_bus_ent_id)})
        #     return gsgs_info
        #
        # def get_qynb_list(self, reg_bus_ent_id):
        #     # 企业年报
        #     response = self._client.get_qynb_list(reg_bus_ent_id)
        #     soup = BeautifulSoup(response.content, 'lxml')
        #     pass
        #
        # def get_gdcz_list(self, reg_bus_ent_id):
        #     response = self._client.get_gdcz_list(reg_bus_ent_id)
        #     soup = BeautifulSoup(response.content, 'lxml')
        #     pass
        #
        # def get_gqbg_list(self, reg_bus_ent_id):
        #     response = self._client.get_gqbg_list(reg_bus_ent_id)
        #     soup = BeautifulSoup(response.content, 'lxml')
        #     pass
        #
        # def get_xzxk_list(self, reg_bus_ent_id):
        #     response = self._client.get_xzxk_list(reg_bus_ent_id)
        #     soup = BeautifulSoup(response.content, 'lxml')
        #     pass
        #
        # def get_zscq_list(self, reg_bus_ent_id):
        #     response = self._client.get_zscq_list(reg_bus_ent_id)
        #     soup = BeautifulSoup(response.content, 'lxml')
        #     pass
        #
        # def get_xzcf_list(self, reg_bus_ent_id):
        #     response = self._client.get_xzcf_list(reg_bus_ent_id)
        #     soup = BeautifulSoup(response.content, 'lxml')
        #     pass
