# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from base_push import BasePush


class ZzjgdmPush(BasePush):
    def __init__(self):
        BasePush.__init__(self)

    def get_templ(self):
        return {
            u"companyName": [u"名称"],
            u'dmzbfjg': [u'代码证颁发机关：'],
            u'zzjgdm': [u'组织机构代码：'],
        }

    def get_pass_list(self):
        return [u'reg_bus_ent_id', u'_id']

    def get_url(self):
        return "https://data.api.zhironghao.com/update/zzjgdm"
