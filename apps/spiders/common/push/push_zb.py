# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from base_push import BasePush


class ZbPush(BasePush):
    def __init__(self):
        BasePush.__init__(self)

    def get_templ(self):
        return {
            u"companyName": [u"名称"],
            u'zczb': [u'注册资本：'],
            u'sszb': [u"实收资本："],
            u'zjczje': [u"实缴出资金额："],
            u'zzsjczsj': [u"最终实缴出资时间："],
            u'zzrjczsj': [u"最终认缴出资时间："],
        }

    def get_pass_list(self):
        return [u'reg_bus_ent_id', u'_id', u'公司公示信息', u'-']

    def get_url(self):
        return "https://data.api.zhironghao.com/update/ziben"
