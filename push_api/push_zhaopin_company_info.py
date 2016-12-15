# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import logging

import pymongo

from bs4 import BeautifulSoup

from push_api import push_data

mongo_client = pymongo.MongoClient()

zhaopin_db = mongo_client["zhaopin"]
company_clean_db = mongo_client['company_clean']

from init_logging import init_logging

_templ = {
    # "company_name": "companyName",  # 公司名称
    # "company_id": "",  # 网站上的ID
    # "city": "province",  # 省份
    # "business_type": "",  # 公司类型
    "people_num": "people",  # 公司规模
    # "business_scope": "",  # 公司行业
    "business_address": "address",  # 公司地址
    "site": "website",  # 公司网站
    "content": "introduce",  # 公司描述

}


def mark_pushed(company_name):
    company_clean_db.company_clean_zhaopin.update(
        {u"company_name": company_name},
        {'$set': {
            u"company_name": company_name,
            u"zhaopin_pushed": 1
        }},
        True, True)


def check_pushed(company_name):
    company = company_clean_db.company_clean_zhaopin.find_one({u"company_name": company_name})
    if company and company.get("zhaopin_pushed") == 1:
        return True
    else:
        return False


def push_extend_info(info, company_name):
    url = "https://data.api.zhironghao.com/update/extendInfo"
    d = dict(info)
    data = {"companyName": company_name, "from": "zhaopin"}
    extend_list = []
    for (k, v) in d.items():
        if k in ["_id", "company_name", "company_id", "city", "business_type", "business_scope"]:
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


province_templ = {
    "beijing": u"北京",
    "shanghai": u"上海",
    "guangzhou": u"广州",
    "shenzhen": u"深圳",
    "tianjin": u"天津",
    "wuhan": u"武汉",
    "xian": u"西安",
    "chengdu": u"成都",
    "dalian": u"大连",
    "changchun": u"长春",
    "shenyang": u"沈阳",
    "nanjing": u"南京",
    "jinan": u"济南",
    "qingdao": u"青岛",
    "hangzhou": u"杭州",
    "suzhou": u"苏州",
    "wuxi": u"无锡",
    "ningbo": u"宁波",
    "chongqing": u"重庆",
    "zhengzhou": u"郑州",
    "changsha": u"长沙",
    "fuzhou": u"福州",
    "xiamen": u"厦门",
    "haerbin": u"哈尔滨",
    "shijiazhuang": u"石家庄",
    "hefei": u"合肥",
    "huizhou": u"惠州",
    "guangdong": u"广东",
    "hubei": u"湖北",
    "shaanxi": u"陕西",
    "sichuan": u"四川",
    "liaoning": u"辽宁",
    "jilin": u"吉林",
    "jiangsu": u"江苏",
    "shandong": u"山东",
    "zhejiang": u"浙江",
    "guangxi": u"广西",
    "anhui": u"安徽",
    "hebei": u"河北",
    "shanxi": u"山西",
    "neimenggu": u"内蒙古",
    "heilongjiang": u"黑龙江",
    "fujian": u"福建",
    "jiangxi": u"江西",
    "henan": u"河南",
    "hunan": u"湖南",
    "hainans": u"海南",
    "guizhou": u"贵州",
    "yunnan": u"云南",
    "tibet": u"西藏",
    "gansu": u"甘肃",
    "qinghai": u"青海",
    "ningxia": u"宁夏",
    "xinjiang": u"新疆",
}


def push_base_info(company_name, province):
    url = "https://data.api.zhironghao.com/update/info"
    data = {
        "companyName": company_name,
        "province": province_templ[province]
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
    cur = zhaopin_db.company_info.find().batch_size(50)

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

            province = company.get("city")
            if province:
                push_base_info(company_name, province)

            push_extend_info(company, company_name)
            # exit(0)
            mark_pushed(company_name)


        except Exception, e:
            logging.exception(e)
            pass

            # exit(-1)


if __name__ == "__main__":
    try:
        init_logging(error_file="log/zhaopin/error.log", info_file="log/zhaopin/info.log",
                     noset_file="log/zhaopin/noset.log")
        push_all()
        # check_templ_all()
        logging.info("finish..........")
    except Exception, e:
        logging.exception(e)
