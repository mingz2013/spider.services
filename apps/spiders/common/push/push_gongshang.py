# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from base_push import BasePush


class GongshangPush(BasePush):
    def __init__(self):
        BasePush.__init__(self)

    def get_templ(self):
        return {
            u"companyName": [u"名称"],
            u"address": [u'住所', u'营业场所', u'经营场所', u'企业住所', u'地址', u'主要经营场所'],
            u"faren": [u'法定代表人', u'经营者姓名', u'经营者', u'法定代表人姓名'],
            u'yyqxZi': [u'营业期限自', u'合伙期限自', u'经营期限自', u'本证有效期限自'],
            u'yyqxZhi': [u'营业期限至', u'合伙期限至', u'经营期限至', u'本证有效期限至'],
            u'type': [u'类型', u'企业类型', u'合伙企业类型', u'公司类型'],
            u'zczj': [u'注册资金', u'成员出资总额', u'注册资本', u'资金数额'],
            u'status': [u'登记状态', u'状态', u'企业状态'],
            u'registerNum': [u'注册号', u'统一社会信用代码'],
            u'tzrName': [u'投资人姓名', u'投资人'],
            u'dxTime': [u'吊销日期', u'注销日期'],
            u'fzr': [u'负责人', u'负责人姓名'],
            u'jyfw': [u'经营范围', u'业务范围'],
            u'djjg': [u'登记机关', u'发照机关'],
            u'createTime': [u'成立日期', u'注册日期'],
            u'fzTime': [u'发照日期'],
            u'bjgslrq': [u'本机构设立日期'],
            u'hzrq': [u'核准日期'],
            u'zxswhhr': [u'执行事务合伙人'],
            u'zxswhhrWpdb': [u'执行事务合伙人（委派代表）'],
            u'sxdbrxx': [u'首席代表人姓名'],
            u'gd': [u'股东（发起人）'],
            u'zcxs': [u'组成形式'],
            u'jjxz': [u'经济性质'],
            u'zzqxz': [u'驻在期限自'],
            u'pcqyMc': [u'派出企业名称'],
            u'pcqyZcd': [u'派出企业注册地'],
            u'gj': [u'国籍'],
            u'lsqy': [u'隶属企业'],
            u'jyfwxxbz': [u'经营范围项下标注']
        }

    def get_pass_list(self):
        return [u'reg_bus_ent_id', u'_id', u'(注不得从事权益类交易、大宗商品交易以及其他标准化合约交易等金融类证券类活动。)']

    def get_url(self):
        return "https://data.api.zhironghao.com/update/gongshang"
