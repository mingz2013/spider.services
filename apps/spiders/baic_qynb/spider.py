# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging
import time

from bs4 import BeautifulSoup

from apps.spiders.common.exception import NeedrefreshProxyError, HttpClientError, ErrorStatusCode

from site_client import SiteClient

from apps.spiders.common.get_search_key import GetSearchKey
from ..common.proxy_pool.proxy_pool import ProxyPool
from ..common.push.push_jichu import GongshangPush, ShuiwuPush, ZbPush, ZzjgdmPush, ShebaoPush


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
                reg_bus_ent_id = self._getSearchKey.get_reg_bus_ent_id()
                # reg_bus_ent_id = item['reg_bus_ent_id']
                logging.info("-------------%s--------------" % reg_bus_ent_id)

                company_info = self.get_company(reg_bus_ent_id)

            except Exception, e:
                logging.exception(e)
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

        self.get_qynb_list(reg_bus_ent_id)

    # ++++++++++++++++++++企业年报+++++++++++begin++++++++++ #
    def get_qynb_list(self, reg_bus_ent_id):
        # 企业年报
        logging.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logging.info("qynb_list reg_bus_ent_id: %s" % reg_bus_ent_id)
        logging.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # 企业年报列表
        response = self._client.get_qynb_list(reg_bus_ent_id)

        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.select_one('table')
        tr_list = table.select('tr')
        tr_list = tr_list[1:]

        qynb_list = []

        for tr in tr_list:
            td_list = tr.select('td')
            assert len(td_list) == 3 or len(td_list) == 1, "assert td_list len "
            if len(td_list) == 1:
                continue

            qynb_info = {
                "number": td_list[0].getText().strip(),  # 序号
                # "year": td_list[1].select_one('a').getText().strip(),  # 报送年度
                "date": td_list[2].getText().strip(),  # 发布日期
            }

            url = None
            try:
                year = td_list[1].select_one('a').getText().strip()  # 报送年度
                url = td_list[1].select_one('a')['onclick'].split('\'')[1]
                url = domain + url
                pass
            except Exception, e:
                year = td_list[1].getText().strip()  # 报送年度
                pass

            qynb_info.update({"year": year})

            if url:
                qynb_detail = self.get_qynb_detail(url)
                qynb_info.update({
                    "qynb_detail": qynb_detail
                })

            qynb_list.append(qynb_info)

        return qynb_list

        pass

    def get_qynb_detail(self, url):
        # 企业年报详细信息
        response = self._client.get_qynb_detail(url)
        soup = BeautifulSoup(response.content, 'lxml')

        qynb_detail = {}

        table_list = soup.select('table[class="detailsList"]')

        assert len(table_list) == 2 or len(table_list) == 1, "table list len: %s" % len(table_list)

        # 企业基本信息
        table_1 = table_list[0]
        th_list = table_1.select('th')
        th_list = th_list[2:]
        # th_list_t = table_1.select('th')
        # th_list.extend(th_list_t)
        # logging.debug(len(th_list))
        td_list = table_1.select('td')
        # td_list_t = table_1.select('td')
        # td_list.extend(td_list_t)
        # logging.debug(len(td_list))
        assert len(th_list) == len(td_list), "th td not =="
        base_info = {}
        for i in range(0, len(th_list)):
            th = th_list[i]
            td = td_list[i]
            base_info.update({
                th.getText().strip(): td.getText().strip()
            })
        qynb_detail.update({"base_info": base_info})
        # logging.debug(qynb_detail)
        # exit(-1)
        if len(table_list) > 1:
            # 企业资产状况信息
            qyzczk_info = {}
            table_2 = table_list[1]
            th_list = table_2.select('tr th')
            th_list = th_list[1:]
            td_list = table_2.select('tr td')
            for i in range(0, len(th_list)):
                th = th_list[i]
                td = td_list[i]
                qyzczk_info.update({
                    th.getText().strip(): td.getText().strip()
                })
            qynb_detail.update({"qyzczk_info": qyzczk_info})

        iframe_list = soup.select('iframe')
        for iframe in iframe_list:
            if iframe['id'] == "gdczFrame":
                # 股东出资
                gdczFrame = iframe  # soup.select_one('iframe[id="gdczFrame"]')
                gdcz_url = domain + gdczFrame['src']
                gdcz_list = self.get_qynb_gdcz_list(gdcz_url)
                qynb_detail.update({"gdcz_list": gdcz_list})
            elif iframe['id'] == 'wzFrame':
                # 网站
                wzFrame = iframe  # soup.select_one('iframe[id="wzFrame"]')
                wz_url = domain + wzFrame['src']
                wz_list = self.get_qynb_wz_list(wz_url)
                qynb_detail.update({"wz_list": wz_list})
            elif iframe['id'] == 'dwdbFrame':
                # 对外投资担保
                dwdbFrame = soup.select_one('iframe[id="dwdbFrame"]')
                dwdb_url = domain + dwdbFrame['src']
                dwdb_list = self.get_qynb_dwdb_list(dwdb_url)
                qynb_detail.update({"dwdb_list": dwdb_list})
            elif iframe['id'] == 'xgFrame':
                # 修改记录
                xgFrame = iframe  # soup.select_one('iframe[id="xgFrame"]')
                xg_url = domain + xgFrame['src']
                xg_list = self.get_qynb_xg_list(xg_url)
                qynb_detail.update({"xg_list": xg_list})
            elif iframe['id'] == 'dwtzFrame':
                # 对外投资
                dwtzFrame = iframe  # soup.select_one('iframe[id="xgFrame"]')
                dwtz_url = domain + dwtzFrame['src']
                dwtz_list = self.get_qynb_dwtz_list(dwtz_url)
                qynb_detail.update({"dwtz_list": dwtz_list})
            elif iframe['id'] == 'gdzrFrame':
                # 股东变更信息
                gdbgFrame = iframe  # soup.select_one('iframe[id="xgFrame"]')
                gdbg_url = domain + gdbgFrame['src']
                gdbg_list = self.get_qynb_gdbg_list(gdbg_url)
                qynb_detail.update({"gdbg_list": gdbg_list})
            else:
                assert False, "iframe id error %s" % iframe['id']

        return qynb_detail

    def get_qynb_gdbg_list(self, url):
        # 股东变更
        response = self._client.get_qynb_gdbg_list(url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.select_one('table')
        tr_list = table.select('tr')
        tr_list = tr_list[2:]
        tr_list = tr_list[:-1]

        gdbg_list = []

        for tr in tr_list:
            td_list = tr.select('td')
            gdbg_info = {
                "gd": td_list[0].getText().strip(),  # 股东
                "bgqbl": td_list[1].getText().strip(),  # 变更前股权比例
                "bghbl": td_list[2].getText().strip(),  # 变更后股权比例
                "bgrq": td_list[3].getText().strip(),  # 股权变更日期
            }
            gdbg_list.append(gdbg_info)

        return gdbg_list

    def get_qynb_dwtz_list(self, url):
        # 对外投资
        response = self._client.get_qynb_dwtz_list(url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.select_one('table')
        tr_list = table.select('tr')
        tr_list = tr_list[2:]
        tr_list = tr_list[:-1]

        dwtz_list = []

        for tr in tr_list:
            td_list = tr.select('td')
            dwtz_info = {
                "name": td_list[0].getText().strip(),  # 投资设立企业或购买股权企业名称
                "code": td_list[1].getText().strip(),  # 注册号/统一社会信用代码
            }
            dwtz_list.append(dwtz_info)

        return dwtz_list

    def get_qynb_xg_list(self, url):
        # 修改记录
        response = self._client.get_qynb_xgjl_list(url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.select_one('table')
        tr_list = table.select('tr')
        tr_list = tr_list[2:]
        tr_list = tr_list[:-1]

        xgjl_list = []

        for tr in tr_list:
            td_list = tr.select('td')
            xgjl_info = {
                "zqr": td_list[0].getText().strip(),  # 序号
                "zwr": td_list[1].getText().strip(),  # 修改事项
                "zzqzl": td_list[2].getText().strip(),  # 修改前
                "zzqse": td_list[3].getText().strip(),  # 修改后
                "lxzwdqx": td_list[4].getText().strip(),  # 修改日期
            }
            xgjl_list.append(xgjl_info)

        return xgjl_list

    def get_qynb_dwdb_list(self, url):
        # 对外担保
        response = self._client.get_qynb_dwdb_list(url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.select_one('table')
        tr_list = table.select('tr')
        tr_list = tr_list[2:]
        tr_list = tr_list[:-1]

        dwdb_list = []

        for tr in tr_list:
            td_list = tr.select('td')
            dwdb_info = {
                "zqr": td_list[0].getText().strip(),  # 债权人
                "zwr": td_list[1].getText().strip(),  # 债务人
                "zzqzl": td_list[2].getText().strip(),  # 主债权种类
                "zzqse": td_list[3].getText().strip(),  # 主债权数额
                "lxzwdqx": td_list[4].getText().strip(),  # 履行债务的期限
                "bzdqj": td_list[5].getText().strip(),  # 保证的期间
                "bzdfs": td_list[6].getText().strip(),  # 保证的方式
                "bzdbdfw": td_list[7].getText().strip(),  # 保证担保的范围
            }
            dwdb_list.append(dwdb_info)

        return dwdb_list

    def get_qynb_gdcz_list(self, url):
        # 股东出资
        response = self._client.get_qynb_gdcz_list(url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.select_one('table')
        tr_list = table.select('tr')
        tr_list = tr_list[2:]
        tr_list = tr_list[:-1]

        gdcz_list = []

        for tr in tr_list:
            td_list = tr.select('td')
            gdcz_info = {
                "gd": td_list[0].getText().strip(),  # 股东
                "rjcze": td_list[1].getText().strip(),  # 认缴出资额(万元)
                "rjczsj": td_list[2].getText().strip(),  # 认缴出资时间
                "rjczfs": td_list[3].getText().strip(),  # 认缴出资方式
                "sjcze": td_list[4].getText().strip(),  # 实缴出资额(万元)
                "sjczsj": td_list[5].getText().strip(),  # 实缴出资时间
                "sjczfs": td_list[6].getText().strip(),  # 实缴出资方式
            }
            gdcz_list.append(gdcz_info)

        return gdcz_list

    def get_qynb_wz_list(self, url):
        # 网站
        response = self._client.get_qynb_wz_list(url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.select_one('table')
        tr_list = table.select('tr')
        tr_list = tr_list[2:]
        tr_list = tr_list[:-1]

        wz_list = []

        for tr in tr_list:
            td_list = tr.select('td')
            wz_info = {
                "lx": td_list[0].getText().strip(),  # 类型
                "mc": td_list[1].getText().strip(),  # 名称
                "wz": td_list[2].getText().strip(),  # 网址
            }
            wz_list.append(wz_info)

        return wz_list

        # ++++++++++++++++++++企业年报+++++++++end++++++++++++ #
