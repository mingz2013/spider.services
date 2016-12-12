# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import logging

from ..common.push_api import push_data


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

    def push_info(self, info, company_name):
        data = {}

        d = dict(info)

        for (k, v) in d.items():
            if k in self._pass_list:
                continue
            is_have = False
            for (kk, vv) in self._templ.items():
                if k in vv:
                    if data.get(kk):
                        logging.error(u"repeat key, %s" % kk)
                        logging.error(d)
                        exit(-1)
                    data.update({kk: v})
                    is_have = True
                    break
            if not is_have:
                logging.error(u"unknown key, %s" % k)
                logging.error(d)
                exit(-1)

        data.update({u"companyName": company_name})

        response = push_data(self._url, data)
        if response.status_code != 200:
            logging.error("error status code: %s" % response.status_code)
            logging.error(d)
            # exit(-1)
            return
        try:
            r = json.loads(response.content)
            returnCode = r.get('returnCode')
            if returnCode == 0:
                logging.info("success.........")
            else:
                logging.error(r)
                # exit(-1)
        except Exception, e:
            logging.exception(e)


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


class ShebaoPush(BasePush):
    def __init__(self):
        BasePush.__init__(self)

    def get_templ(self):
        return {}

    def get_pass_list(self):
        return [u'reg_bus_ent_id', u'_id']

    def get_url(self):
        return "https://data.api.zhironghao.com/update/shebao"
