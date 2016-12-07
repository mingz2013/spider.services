# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging

from bs4 import BeautifulSoup

from exception import NeedrefreshProxyError, HttpClientError, ErrorStatusCode
from get_proxy import GetProxy
from get_search_key import GetSearchKey
from mongo import QyxybaicLevel3DB
from site_client import SiteClient


# 公司公示信息 除了企业年报之外的所有
class Spider(object):
    def __init__(self):
        self._client = SiteClient()
        self._getProxy = GetProxy(3, 0)
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
                    if QyxybaicLevel3DB.get_one(reg_bus_ent_id):
                        logging.info("----------------is have-------------------")
                        continue

                    company = {"reg_bus_ent_id": reg_bus_ent_id}
                    company_info = self.get_company(reg_bus_ent_id)
                    company.update(company_info)
                    QyxybaicLevel3DB.upsert_company_detail_level_3(company)
                except NeedrefreshProxyError, err:
                    self._refresh_proxy()
                    continue
                except ErrorStatusCode, err:
                    self._refresh_proxy()
                    continue
                except HttpClientError, err:
                    self._refresh_proxy()
                    continue
                    # except Exception, e:
                    #     self._refresh_proxy()
                    #     continue

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

        # company.update({"other_info": self.get_other_info(reg_bus_ent_id)})
        company.update({"gsgs_info": self.get_gsgs_info(reg_bus_ent_id)})

        return company

    # ++++++++公司公示信息+++++++++++++++++++++++++ #
    def get_gsgs_info(self, reg_bus_ent_id):
        logging.info("get_gsgs_info..............")
        # 公司公示信息
        gsgs_info = {}
        # gsgs_info.update({"qynb": self.get_qynb_list(reg_bus_ent_id)})
        gsgs_info.update({"gdcz": self.get_gdcz_list(reg_bus_ent_id)})
        gsgs_info.update({"gqbg": self.get_gdbg_list(reg_bus_ent_id)})
        gsgs_info.update({"xzxk": self.get_xzxk_list(reg_bus_ent_id)})
        gsgs_info.update({"zscq": self.get_zscq_list(reg_bus_ent_id)})
        gsgs_info.update({"xzcf": self.get_xzcf_list(reg_bus_ent_id)})
        return gsgs_info

    def get_gdcz_list(self, reg_bus_ent_id):
        logging.info("get_gdcz_list..............")
        # 股东及出资信息
        response = self._client.get_gdcz_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        print response.content
        gdcz_list = []
        tr_list = soup.select('table[id="tableIdStyle"] > tr')
        tr_list = tr_list[2:]
        logging.debug("len %s" % len(tr_list))
        for tr in tr_list:
            td_list = tr.select('> td')
            if len(td_list) == 5:
                gdcz_info = {}
                gdcz_info.update({
                    "gd": td_list[0].getText().strip(),  # 股东
                    "rje": td_list[1].getText().strip(),  # 认缴额(万元)
                    "sje": td_list[2].getText().strip(),  # 实缴额(万元)
                    "rjmx_list": self.get_gdcz_rjmx_list(td_list[3]),  # 认缴明细
                    "sjmx_list": self.get_gdcz_sjmx_list(td_list[4])  # 实缴明细
                })
                gdcz_list.append(gdcz_info)
        return gdcz_list

    def get_gdcz_rjmx_list(self, td):
        # 认缴明细
        tr_list = td.select('table tr')
        rjmx_list = []
        logging.debug("len %s" % len(tr_list))
        for tr in tr_list:
            td_list = tr.select('td')
            rjmx_list.append({
                "czfs": td_list[0].getText().strip(),  # 认缴出资方式
                "cze": td_list[1].getText().strip(),  # 认缴出资额(万元)
                "czrq": td_list[2].getText().strip(),  # 认缴出资日期
            })
        return rjmx_list

    def get_gdcz_sjmx_list(self, td):
        # 实缴明细
        tr_list = td.select('table tr')
        sjmx_list = []
        logging.debug("len %s" % len(tr_list))
        for tr in tr_list:
            td_list = tr.select('td')
            sjmx_list.append({
                "czfs": td_list[0].getText().strip(),  # 实缴出资方式
                "cze": td_list[1].getText().strip(),  # 实缴出资额(万元)
                "czrq": td_list[2].getText().strip(),  # 实缴出资日期
            })
        return sjmx_list

    def get_gdbg_list(self, reg_bus_ent_id):
        logging.info("get_gdbg_list..............")
        # 股东变更
        response = self._client.get_gqbg_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        gdbg_list = []
        tr_list = soup.select('table[id="tableIdStyle"] tr')
        tr_list = tr_list[1:]
        logging.debug("len %s" % len(tr_list))
        for tr in tr_list:
            td_list = tr.select('td')
            if len(td_list) == 5:
                gdbg_info = {
                    "number": td_list[0].getText().strip(),  # 序号
                    "gd": td_list[1].getText().strip(),  # 股东
                    "bgqbl": td_list[2].getText().strip(),  # 变更前股权比例
                    "bghbl": td_list[3].getText().strip(),  # 变更后股权比例
                    "bgrq": td_list[4].getText().strip(),  # 股权变更日期
                }
                gdbg_list.append(gdbg_info)
        if len(tr_list) > 1:
            logging.debug(gdbg_list)
            logging.debug("tr_list > 1, parse it!!")
            exit(1)
        return gdbg_list

    def get_xzxk_list(self, reg_bus_ent_id):
        logging.info("get_xzxk_list..............")
        # 行政许可
        response = self._client.get_xzxk_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        xzxk_list = []
        tr_list = soup.select('table[id="tableIdStyle"] tr')
        tr_list = tr_list[1:]
        logging.debug("len %s" % len(tr_list))
        for tr in tr_list:
            td_list = tr.select('td')
            if len(td_list) == 9:
                xzxk_info = {
                    "number": td_list[0].getText().strip(),  # 序号
                    "xkwjbh": td_list[1].getText().strip(),  # 许可文件编号
                    "xkwjmc": td_list[2].getText().strip(),  # 许可文件名称
                    "yxqzi": td_list[3].getText().strip(),  # 有效期自
                    "yxqzhi": td_list[4].getText().strip(),  # 有效期至
                    "xkjg": td_list[5].getText().strip(),  # 许可机关
                    "xknr": td_list[6].getText().strip(),  # 许可内容
                    "zt": td_list[7].getText().strip(),  # 状态
                    "xq": td_list[8].getText().strip(),  # 详情
                }
                xzxk_list.append(xzxk_info)
        if len(tr_list) > 1:
            logging.debug(xzxk_list)
            logging.debug("tr_list > 1, parse it!!")
            exit(1)
        return xzxk_list

    def get_zscq_list(self, reg_bus_ent_id):
        logging.info("get_zscq_list..............")
        # 知识产权
        response = self._client.get_zscq_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        zscq_list = []
        tr_list = soup.select('table[id="tableIdStyle"] tr')
        tr_list = tr_list[1:]
        logging.debug("len %s" % len(tr_list))
        for tr in tr_list:
            td_list = tr.select('td')
            if len(td_list) == 9:
                zscq_info = {
                    "number": td_list[0].getText().strip(),  # 序号
                    "zch": td_list[1].getText().strip(),  # 注册号
                    "mc": td_list[2].getText().strip(),  # 名称
                    "zl": td_list[3].getText().strip(),  # 种类
                    "czrmc": td_list[4].getText().strip(),  # 出质人名称
                    "zqrmc": td_list[5].getText().strip(),  # 质权人名称
                    "zqdjqx": td_list[6].getText().strip(),  # 质权登记期限
                    "zt": td_list[7].getText().strip(),  # 状态
                    "bhqk": td_list[8].getText().strip(),  # 变化情况
                }
                zscq_list.append(zscq_info)
        if len(tr_list) > 1:
            logging.debug(zscq_list)
            logging.debug("tr_list > 1, parse it!!")
            exit(1)
        return zscq_list

    def get_xzcf_list(self, reg_bus_ent_id):
        logging.info("get_xzcf_list..............")
        # 行政处罚
        response = self._client.get_xzcf_list(reg_bus_ent_id)
        soup = BeautifulSoup(response.content, 'lxml')
        xzcf_list = []
        tr_list = soup.select('table[id="tableIdStyle"] tr')
        tr_list = tr_list[1:]
        logging.debug("len %s" % len(tr_list))
        for tr in tr_list:
            td_list = tr.select('td')
            if len(td_list) == 8:
                xzcf_info = {
                    "number": td_list[0].getText().strip(),  # 序号
                    "xzcfjdswh": td_list[1].getText().strip(),  # 行政处罚决定书文号
                    "xzcfnr": td_list[2].getText().strip(),  # 行政处罚内容
                    "zcxzcfjdjgmc": td_list[3].getText().strip(),  # 做出行政处罚决定机关名称
                    "zcxzcfjdrq": td_list[4].getText().strip(),  # 做出行政处罚决定日期
                    "wfxwlx": td_list[5].getText().strip(),  # 违法行为类型
                    "bz": td_list[6].getText().strip(),  # 备注
                    "xq": td_list[7].getText().strip(),  # 详情
                }
                xzcf_list.append(xzcf_info)
        if len(tr_list) > 1:
            logging.debug(xzcf_list)
            logging.debug("tr_list > 1, parse it!!")
            exit(1)
        return xzcf_list
