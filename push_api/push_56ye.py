# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import logging

import pymongo

from bs4 import BeautifulSoup

from push_api import push_data

mongo_client = pymongo.MongoClient()

_56ye_db = mongo_client["56ye"]
company_clean_db = mongo_client['company_clean']

from init_logging import init_logging

_templ = {

    "people_num": "people",  # 公司规模
    "business_address": "address",  # 公司地址
    # "url": "website",  # 公司网站
    "introduce": "introduce",  # 公司描述
    "phone": "phone",  # 电话

}


def mark_pushed(company_name):
    company_clean_db.company_clean_56ye.update(
        {u"company_name": company_name},
        {'$set': {
            u"company_name": company_name,
            u"56ye_pushed": 1
        }},
        True, True)


def check_pushed(company_name):
    company = company_clean_db.company_clean_56ye.find_one({u"company_name": company_name})
    if company and company.get("56ye_pushed") == 1:
        return True
    else:
        return False


def push_extend_info(info, company_name):
    url = "https://data.api.zhironghao.com/update/extendInfo"
    d = dict(info)
    data = {"companyName": company_name, "from": "56ye"}
    extend_list = []
    for (k, v) in d.items():
        if k in ["_id", "province", "city", "company_name", "registered_capital", "register_date", "business_type",
                 "business_scope", "link_man"]:
            continue
        if k in _templ.keys():
            e = {
                "type": _templ.get(k),
                "content": v,
            }
            if e.get("type") == "introduce":
                e.update({
                    "content": BeautifulSoup(e.get("content"), 'lxml').getText()
                })
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


def push_base_info(company_name, province=None, city=None, district=None):
    url = "https://data.api.zhironghao.com/update/info"
    data = {
        "companyName": company_name,
        "province": province,
        "city": city,
        "district": district
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
    cur = _56ye_db.company_info_items.find().batch_size(50)

    for company in cur:
        try:
            company = dict(company)
            company_name = company.get("company_name")
            if not company_name:
                logging.error("not found company_name...")
                continue

            if check_pushed(company_name):
                logging.info("pass........")
                continue

            province = company.get("province")
            logging.debug(province)
            province = province[1:-1]

            city = company.get("city")
            if city:
                if city.find('/') >= 0:
                    city = city.split('/')[1]

            push_base_info(company_name, province, city)

            push_extend_info(company, company_name)
            # exit(0)
            mark_pushed(company_name)

        except Exception, e:
            logging.exception(e)
            logging.error(company)
            # exit(-1)


if __name__ == "__main__":
    try:
        init_logging(error_file="log/56ye/error.log", info_file="log/56ye/info.log",
                     noset_file="log/56ye/noset.log")
        push_all()
        # check_templ_all()
        logging.info("finish..........")
    except Exception, e:
        logging.exception(e)
