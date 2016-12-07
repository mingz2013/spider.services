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

gongshang_templ = {
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


def check_templ(gsdjzc_info):
    for (kk, vv) in gongshang_templ.items():
        if len(vv) > 1:
            d = dict(gsdjzc_info)
            tmp = list(set(vv).intersection(set(d.keys())))
            if len(tmp) > 1:
                logging.info(tmp)
            pass
    pass


def mark_gongshang_pushed(company_name, reg_bus_ent_id):
    company_clean_db.company_clean.update(
        {u"reg_bus_ent_id": reg_bus_ent_id},
        {'$set': {
            u"company_name": company_name,
            u"reg_bus_ent_id": reg_bus_ent_id,
            u"gongshang_pushed": 1
        }},
        True, True)


def check_gongshang_pushed(reg_bus_ent_id):
    company = company_clean_db.company_clean.find_one({u"reg_bus_ent_id": reg_bus_ent_id})
    if company and company.get("gongshang_pushed") == 1:
        return True
    else:
        return False


def push_gongshang(gsdjzc_info, reg_bus_ent_id):
    if check_gongshang_pushed(reg_bus_ent_id):
        logging.info("pass........")
        return

    url = "https://data.api.zhironghao.com/update/gongshang"
    data = {}

    d = dict(gsdjzc_info)

    for (k, v) in d.items():
        if k in [u'reg_bus_ent_id', u'_id', u'(注不得从事权益类交易、大宗商品交易以及其他标准化合约交易等金融类证券类活动。)']:
            continue
        is_have = False
        for (kk, vv) in gongshang_templ.items():
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
            mark_gongshang_pushed(data.get("companyName"), reg_bus_ent_id)
            logging.info("success.........")
        else:
            logging.error(r)
            # exit(-1)
    except Exception, e:
        logging.exception(e)


def push_gongshang_all():
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
        push_gongshang(gsdjzc_info, reg_bus_ent_id)

        # break  # 只push一次测试


def check_templ_all():
    '''
    检查模板是否正确,比如多个要合并的字段,是否会同时出现在一个公司里
    :return:
    '''
    cur = qyxy_baic_db.company_info.find().batch_size(50)

    for company in cur:

        base_info = company.get("base_info")
        if not base_info:
            continue
        gsdjzc_info = base_info.get("gsdjzc_info")
        if gsdjzc_info:
            check_templ(gsdjzc_info)

            # break  # 只push一次测试


if __name__ == "__main__":
    try:
        init_logging(error_file="log/gongshang/error.log", info_file="log/gongshang/info.log",
                     noset_file="log/gongshang/noset.log")
        push_gongshang_all()
        # check_templ_all()
        logging.info("finish..........")
    except Exception, e:
        logging.exception(e)
