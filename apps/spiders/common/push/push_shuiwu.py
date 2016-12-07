# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from base_push import BasePush


class ShuiwuPush(BasePush):
    def __init__(self):
        BasePush.__init__(self)

    def get_templ(self):
        return {
            u"companyName": [u"名称"],
            u"swdjzh": [u"税务登记证号"],
            u"yb": [u"经营地址邮编"],
            u"swdjlx": [u"税务登记类型"],
            u"djsllx": [u"登记受理类型"],
            u"jydz": [u"经营地址"],
            u"jydzPhone": [u"经营地址联系电话"],
            u"scjx": [u"所处街乡"],
            u"gdsgghbs": [u"国地税共管户标识"],
            u"lsgx": [u"隶属关系"],
            u"gjbzhy": [u"国家标准行业"],
            u"swdjrq": [u"税务登记日期"],
            u"zgswjg": [u"主管税务机关"],
            u"nsrStatus": [u"纳税人状态"],
            u"nsrName": [u"纳税人名称"],
            u"zch": [u"注册号"],
            u"zzjgdm": [u"组织机构代码"],
            u"djzclx": [u"登记注册类型"],
            u"qyzywz": [u"企业主页网址"],
            u"faren": [u"法人姓名"],
        }

    def get_pass_list(self):
        return [u'reg_bus_ent_id', u'_id']

    def get_url(self):
        return "https://data.api.zhironghao.com/update/shuiwu"
