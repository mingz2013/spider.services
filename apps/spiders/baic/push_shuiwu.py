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


# def check_templ(gsdjzc_info):
#     for (kk, vv) in gongshang_templ.items():
#         if len(vv) > 1:
#             d = dict(gsdjzc_info)
#             tmp = list(set(vv).intersection(set(d.keys())))
#             if len(tmp) > 1:
#                 logging.info(tmp)
#             pass
#     pass


def mark_pushed(company_name, reg_bus_ent_id):
    company_clean_db.company_clean.update(
        {u"reg_bus_ent_id": reg_bus_ent_id},
        {'$set': {
            u"company_name": company_name,
            u"reg_bus_ent_id": reg_bus_ent_id,
            u"sw_pushed": 1
        }},
        True, True)


def check_pushed(reg_bus_ent_id):
    company = company_clean_db.company_clean.find_one({u"reg_bus_ent_id": reg_bus_ent_id})
    if company and company.get("sw_pushed") == 1:
        return True
    else:
        return False


def push_zb(gsdjzc_info, reg_bus_ent_id, company_name):
    if check_pushed(reg_bus_ent_id):
        logging.info("pass........")
        return

    url = "https://data.api.zhironghao.com/update/shuiwu"
    data = {}

    d = dict(gsdjzc_info)

    for (k, v) in d.items():
        if k in [u'reg_bus_ent_id', u'_id']:
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
            mark_pushed(company_name, reg_bus_ent_id)
            logging.info("success.........")
        else:
            logging.error(r)
            # exit(-1)
    except Exception, e:
        logging.exception(e)


def push_all():
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
        swdj_info = base_info.get("swdj_info")
        if not swdj_info:
            logging.error("not found swdj_info....%s" % reg_bus_ent_id)
            continue

        push_zb(swdj_info, reg_bus_ent_id, company_name)

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
        init_logging(error_file="log/swdj/error.log", info_file="log/swdj/info.log",
                     noset_file="log/swdj/noset.log")
        push_all()
        # check_templ_all()
        logging.info("finish..........")
    except Exception, e:
        logging.exception(e)
