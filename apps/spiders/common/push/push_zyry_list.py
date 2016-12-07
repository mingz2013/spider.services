# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import logging

import pymongo

from push_api import push_data

mongo_client = pymongo.MongoClient()

qyxy_baic_db = mongo_client["qyxy_baic"]
company_clean_db = mongo_client['company_clean']


def mark_pushed(company_name, reg_bus_ent_id):
    company_clean_db.company_clean.update(
        {u"reg_bus_ent_id": reg_bus_ent_id},
        {'$set': {
            u"company_name": company_name,
            u"reg_bus_ent_id": reg_bus_ent_id,
            u"zyry_pushed": 1
        }},
        True, True)


def check_pushed(reg_bus_ent_id):
    company = company_clean_db.company_clean.find_one({u"reg_bus_ent_id": reg_bus_ent_id})
    if company and company.get(u"zyry_pushed") == 1:
        return True
    else:
        return False


info_templ = {
    u"name": u"name",
    u"position": u"position",
    u"sex": u"sex",
}


def push_zyry_list(info_list, reg_bus_ent_id, company_name):
    if check_pushed(reg_bus_ent_id):
        logging.info("pass........")
        return

    # url = "https://data.api.zhironghao.com/update/qiyenianbao"
    url = "https://data.api.zhironghao.com/update/zhuyaorenyuan"

    d = list(info_list)
    data = {}
    l = []
    for tzr in d:
        i = {}
        for (k, v) in tzr.items():
            if k in [u"number"]:
                continue
            if k in info_templ.keys():
                i.update({
                    info_templ.get(k): v
                })
            else:
                logging.error("not have k in templ in push_zyry_list  ...k:%s" % k)
                exit(-1)
        l.append(i)

    data.update({
        u"companyName": company_name,
        u"info": json.dumps(l),
    })

    response = push_data(url, data)
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
        mark_pushed(company_name, reg_bus_ent_id)
        logging.info("success.........")
    else:
        logging.error(r)
        # exit(-1)
