# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import logging

from push_api import push_data

_templ = {
    u"companyName": [u"名称"],
    u'dmzbfjg': [u'代码证颁发机关：'],
    u'zzjgdm': [u'组织机构代码：'],
}

pass_list = [u'reg_bus_ent_id', u'_id']

url = "https://data.api.zhironghao.com/update/zzjgdm"


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
