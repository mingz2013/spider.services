# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import logging

from push_api import push_data

_templ = {
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

pass_list = [u'reg_bus_ent_id', u'_id']

url = "https://data.api.zhironghao.com/update/shuiwu"


def push_info(info, company_name):
    data = {}

    d = dict(info)

    for (k, v) in d.items():
        if k in pass_list:
            continue
        is_have = False
        for (kk, vv) in _templ.items():
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

    response = push_data(url, data)
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
