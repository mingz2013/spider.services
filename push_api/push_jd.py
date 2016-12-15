# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import logging

import pymongo

from bs4 import BeautifulSoup

from push_api import push_data

mongo_client = pymongo.MongoClient()

jd_db = mongo_client["jd"]
company_clean_db = mongo_client['company_clean']

from init_logging import init_logging

_templ = {
    # "company_name": "companyName",  # 公司名称
    # "company_id": "",  # 网站上的ID
    # "city": "province",  # 省份
    # "business_type": "",  # 公司类型
    # "people_num": "people",  # 公司规模
    # "business_scope": "",  # 公司行业
    # "business_address": "address",  # 公司地址
    "sheller_url": "website",  # 公司网站
    "category": "introduce",  # 公司描述
    "sheller_phone": "phone",  # 电话

}


def mark_pushed(company_name):
    company_clean_db.company_clean_jd.update(
        {u"company_name": company_name},
        {'$set': {
            u"company_name": company_name,
            u"jd_pushed": 1
        }},
        True, True)


def check_pushed(company_name):
    company = company_clean_db.company_clean_jd.find_one({u"company_name": company_name})
    if company and company.get("jd_pushed") == 1:
        return True
    else:
        return False


def push_extend_info(info, company_name):
    url = "https://data.api.zhironghao.com/update/extendInfo"
    d = dict(info)
    data = {"companyName": company_name, "from": "jd"}
    extend_list = []
    for (k, v) in d.items():
        if k in ["_id", "insert_time", "shop_name", "sheller_name", "shop_address"]:
            continue
        if k in _templ.keys():
            e = {
                "type": _templ.get(k),
                "content": v,
            }
            # if e.get("type") == "introduce":
            #     e.update({
            #         "content": BeautifulSoup(e.get("content"), 'lxml').getText()
            #     })
            extend_list.append(e)
        else:
            logging.error("unknwn key %s" % k)
            exit(-1)
    data.update({
        "info": json.dumps(extend_list)
    })

    response = push_data(url, data)
    if response.status_code != 200:
        logging.error("error status code: %s" % response.status_code)
        logging.error("%s" % data)
        # exit(-1)
        raise Exception("status code error")
    try:
        # logging.info(response.content)
        r = json.loads(response.content)
        # {"returnCode":0}
        returnCode = r.get('returnCode')
        if returnCode == 0:
            logging.info("success.........")
        else:
            logging.error(r)
            raise Exception("returnCode error")
    except Exception, e:
        logging.exception(e)
        raise Exception("json loads error")


def push_base_info(company_name, province, city):
    url = "https://data.api.zhironghao.com/update/info"
    data = {
        "companyName": company_name,
        "province": province,
        "city": city
    }
    response = push_data(url, data)
    if response.status_code != 200:
        logging.error("error status code: %s" % response.status_code)
        logging.error("%s" % data)
        # exit(-1)
        raise Exception("status code error")
    try:
        # logging.info(response.content)
        r = json.loads(response.content)
        # {"returnCode":0}
        returnCode = r.get('returnCode')
        if returnCode == 0:
            logging.info("success.........")
        else:
            logging.error(r)
            raise Exception("returnCode error")
    except Exception, e:
        logging.exception(e)
        raise Exception("json loads error")


def push_all():
    cur = jd_db.sheller_info_items.find().batch_size(50)

    for company in cur:
        try:
            company = dict(company)
            company_name = company.get("shop_name")
            if not company_name:
                logging.error("not found company_name...")
                continue

            if check_pushed(company_name):
                logging.info("pass........")
                continue

            shop_address = company.get("shop_address")
            if shop_address:
                p_c = shop_address.split()
                push_base_info(company_name, p_c[0], p_c[1])

            push_extend_info(company, company_name)
            # exit(0)
            mark_pushed(company_name)


        except Exception, e:
            logging.exception(e)
            pass

            # exit(-1)


if __name__ == "__main__":
    try:
        init_logging(error_file="log/jd/error.log", info_file="log/jd/info.log",
                     noset_file="log/jd/noset.log")
        push_all()
        # check_templ_all()
        logging.info("finish..........")
    except Exception, e:
        logging.exception(e)
