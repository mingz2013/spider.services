# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging

import pymongo
import json

from push_api import push_data

mongo_client = pymongo.MongoClient()

qyxy_baic_db = mongo_client["qyxy_baic"]
company_clean_db = mongo_client['company_clean']

from init_logging import init_logging

_templ = {
    u"companyName": [u"名称"],
    u'zczb': [u'注册资本：'],
    u'sszb': [u"实收资本："],
    u'zjczje': [u"实缴出资金额："],
    u'zzsjczsj': [u"最终实缴出资时间："],
    u'zzrjczsj': [u"最终认缴出资时间："],
}


# def check_templ(gsdjzc_info):
#     for (kk, vv) in gongshang_templ.items():
#         if len(vv) > 1:
#             d = dict(gsdjzc_info)
#             tmp = list(set(vv).intersection(set(d.keys())))
#             if len(tmp) > 1:
#                 logging.info(tmp)
#             pass
#     pass


def mark_zb_pushed(company_name, reg_bus_ent_id):
    company_clean_db.company_clean.update(
        {u"reg_bus_ent_id": reg_bus_ent_id},
        {'$set': {
            u"company_name": company_name,
            u"reg_bus_ent_id": reg_bus_ent_id,
            u"zb_pushed": 1
        }},
        True, True)


def check_zb_pushed(reg_bus_ent_id):
    company = company_clean_db.company_clean.find_one({u"reg_bus_ent_id": reg_bus_ent_id})
    if company and company.get("zb_pushed") == 1:
        return True
    else:
        return False


def push_zb(gsdjzc_info, reg_bus_ent_id, company_name):
    if check_zb_pushed(reg_bus_ent_id):
        logging.info("pass........")
        return

    url = "https://data.api.zhironghao.com/update/ziben"
    data = {}

    d = dict(gsdjzc_info)

    for (k, v) in d.items():
        if k in [u'reg_bus_ent_id', u'_id', u'公司公示信息', u'-']:
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
        # logging.info(response.content)
        r = json.loads(response.content)
        # {"returnCode":0}
        returnCode = r.get('returnCode')
        if returnCode == 0:
            mark_zb_pushed(company_name, reg_bus_ent_id)
            logging.info("success.........")
        else:
            logging.error(r)
            # exit(-1)
    except Exception, e:
        logging.exception(e)


def push_zb_all():
    cur = qyxy_baic_db.company_info.find().batch_size(50)

    for company in cur:

        base_info = company.get("base_info")
        reg_bus_ent_id = company.get("reg_bus_ent_id")
        if not base_info:
            logging.error("not found base info....%s" % reg_bus_ent_id)
            continue
        gsdjzc_info = base_info.get("gsdjzc_info")
        if not gsdjzc_info:
            logging.error("not found gsdjzc_info....%s" % reg_bus_ent_id)
            continue
        company_name = gsdjzc_info.get(u"名称")
        if not company_name:
            logging.error("not found company_name....%s" % reg_bus_ent_id)
            continue
        zbxg_info = base_info.get("zbxg_info")
        if not zbxg_info:
            logging.error("not found zbxg_info....%s" % reg_bus_ent_id)
            continue

        push_zb(zbxg_info, reg_bus_ent_id, company_name)

        # break  # 只push一次测试


# def check_templ_all():
#     '''
#     检查模板是否正确,比如多个要合并的字段,是否会同时出现在一个公司里
#     :return:
#     '''
#     cur = qyxy_baic_db.company_info.find().batch_size(50)
#
#     for company in cur:
#
#         base_info = company.get("base_info")
#         if not base_info:
#             continue
#         gsdjzc_info = base_info.get("gsdjzc_info")
#         if gsdjzc_info:
#             check_templ(gsdjzc_info)
#
#             # break  # 只push一次测试


if __name__ == "__main__":
    try:
        init_logging(error_file="log/zb/error.log", info_file="log/zb/info.log", noset_file="log/zb/noset.log")
        push_zb_all()
        # check_templ_all()
        logging.info("finish..........")
    except Exception, e:
        logging.exception(e)
