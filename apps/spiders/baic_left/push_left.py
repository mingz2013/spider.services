# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import logging

from push_api import push_data


class BasePush(object):
    def __init__(self):
        self._pass_list = self.get_pass_list()
        self._templ = self.get_templ()
        self._url = self.get_url()
        pass

    def get_pass_list(self):
        assert False, "need to be overwrite"
        return []

    def get_templ(self):
        assert False, "need to be overwrite"
        return {}

    def get_url(self):
        assert False, "need to be overwrite"
        return ""

    def push_list(self, info_list, company_name):
        d = list(info_list)
        data = {}
        l = []
        for info in d:
            i = {}
            for (k, v) in info.items():
                if k in self._pass_list:
                    continue
                if k in self._templ.keys():
                    i.update({
                        self._templ.get(k): v
                    })
                else:
                    logging.error("not have k in templ in push_tzr_history_list  ...k:%s" % k)
                    exit(-1)
            l.append(i)

        data.update({
            u"companyName": company_name,
            u"info": json.dumps(l),
        })

        response = push_data(self._url, data)
        if response.status_code != 200:
            logging.error("error status code: %s" % response.status_code)
            logging.error(d)
            # exit(-1)
            return

        # logging.info(response.content)
        r = json.loads(response.content)
        # {"returnCode":0}
        returnCode = r.get('returnCode')
        if returnCode == 0:
            logging.info("success.........")
        else:
            logging.error(r)
            # exit(-1)


class TzrPush(BasePush):
    def __init__(self):
        BasePush.__init__(self)

    def get_pass_list(self):
        return [u"number"]

    def get_templ(self):
        return {
            u"name": u"tzrName",
            u"card_type": u"zzType",
            u"card_number": u"zzNum",
            u"investor_type": u"tzrType",

        }

    def get_url(self):
        return "https://data.api.zhironghao.com/update/touziren"


class TzrHistoryPush(BasePush):
    def __init__(self):
        BasePush.__init__(self)

    def get_pass_list(self):
        return [u"number"]

    def get_templ(self):
        return {
            u"name": u"tzrName",
            u"investor_type": u"tzrType",
            u"subscription_time": u"rjczTime",
            u"subscription_mode": u"rjczType",
            u"subscription_amount": u"rjczPrice",
            u"paid_time": u"sjczTime",
            u"paid_mode": u"sjczType",
            u"paid_amount": u"sjczPrice",
        }

    def get_url(self):
        return "https://data.api.zhironghao.com/update/chuzilishi"


class ZtzPush(BasePush):
    def __init__(self):
        BasePush.__init__(self)

    def get_pass_list(self):
        return [u"number"]

    def get_templ(self):
        return {
            u"company_name": u"companyName",  # 主体名称
            u"zch": u"registerNum",  # 注册号
            u"fddbr": u"faren",  # 法定代表人
            u"address": u"address",  # 地址

        }

    def get_url(self):
        return "https://data.api.zhironghao.com/update/zaitouzi"


class ZyryPush(BasePush):
    def __init__(self):
        BasePush.__init__(self)

    def get_pass_list(self):
        return [u"number"]

    def get_templ(self):
        return {
            u"name": u"name",
            u"position": u"position",
            u"sex": u"sex",

        }

    def get_url(self):
        return "https://data.api.zhironghao.com/update/zhuyaorenyuan"
