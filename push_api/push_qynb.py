# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import logging

import pymongo

from push_api import push_data

mongo_client = pymongo.MongoClient()

qyxy_baic_db = mongo_client["qyxy_baic"]
company_clean_db = mongo_client['company_clean']

from init_logging import init_logging


def mark_pushed(company_name, reg_bus_ent_id):
    company_clean_db.company_clean.update(
        {u"reg_bus_ent_id": reg_bus_ent_id},
        {'$set': {
            u"company_name": company_name,
            u"reg_bus_ent_id": reg_bus_ent_id,
            u"qynb_pushed": 1
        }},
        True, True)


def check_pushed(reg_bus_ent_id):
    company = company_clean_db.company_clean.find_one({u"reg_bus_ent_id": reg_bus_ent_id})
    if company and company.get(u"qynb_pushed") == 1:
        return True
    else:
        return False


company_base_info_templ = {
    u"企业经营状态": u"status",
    u"注册号/统一社会信用代码": u"registerNum",
    u"企业名称": u"companyName",
    u"电子邮箱": u"email",
    u"从业人数": u"peopleNum",
    u"企业联系电话": u"phone",
    u"企业是否有投资信息或购买其他公司股权": u"isHaveTzxx",
    u"企业通信地址": u"address",
    u"是否有网站或网店": u"isHaveWebsite",
    u"邮政编码": u"zipcode",
    u"有限责任公司本年度是否发生股东股权转让": u"isGqzr"
}


def parse_company_base_info(company_base_info):
    result = {}
    if not company_base_info:
        return result

    for (k, v) in company_base_info.items():
        if k == "":
            continue
        if k in company_base_info_templ.keys():
            result.update({
                company_base_info_templ.get(k): v
            })
        else:
            logging.error("not have k in templ in company_base info ...k:%s" % k)
            exit(-1)
    return result


qyzczk_info_templ = {
    u"营业总收入中主营业务收入": u"yyzsrzzyywsr",
    u"纳税总额": u"nsze",
    u"负债总额": u"fzze",
    u"所有者权益合计": u"syzqyhj",
    u"销售总额": u"xsze",
    u"资产总额": u"zczr",
    u"利润总额": u"lrze",
    u"净利润": u"jlr"
}


def parse_qyzczk_info(qyzczk_info):
    result = {}
    if not qyzczk_info:
        return result

    for (k, v) in qyzczk_info.items():
        if k in qyzczk_info_templ.keys():
            result.update({
                qyzczk_info_templ.get(k): v
            })
        else:
            logging.error("not have k in templ in qyzczk_info  ...k:%s" % k)
            exit(-1)
    return result


gdcz_info_templ = {
    u"gd": u"gdName",
    u"sjczsj": u"sjczTime",
    u"sjczfs": u"sjczType",
    u"sjcze": u"sjczPrice",
    u"rjczsj": u"rjczTime",
    u"rjczfs": u"rjczType",
    u"rjcze": u"rjczPrice"
}


def parse_gdcz_info_list(gdcz_info_list):
    result = []
    if not gdcz_info_list:
        return result
    for info in gdcz_info_list:
        i = {}
        for (k, v) in info.items():
            if k in gdcz_info_templ.keys():
                i.update({
                    gdcz_info_templ.get(k): v
                })
            else:
                logging.error("not have k in templ in gdcz_info_list  ...k:%s" % k)
                exit(-1)
        result.append(i)
    return result


website_info_templ = {
    u"lx": u"type",
    u"mc": u"name",
    u"wz": u"domain"
}


def parse_website_info_list(website_info_list):
    result = []
    if not website_info_list:
        return result
    for info in website_info_list:
        i = {}
        for (k, v) in info.items():
            if k in website_info_templ.keys():
                i.update({
                    website_info_templ.get(k): v
                })
            else:
                logging.error("not have k in templ in website_info  ...k:%s" % k)
                exit(-1)
        result.append(i)
    return result


dwdb_info_templ = {
    u"zqr": u"zqr",
    u"zwr": u"zwr",
    u"zzqzl": u"zzqzl",
    u"zzqse": u"zzqse",
    u"lxzwdqx": u"lxzwdqx",
    u"bzdqj": u"bzdqj",
    u"bzdfs": u"bzdfs",
    u"bzdbdfw": u"bzdbdfw",
}


def parse_dwdb_list(dwdb_list):
    result = []
    if not dwdb_list:
        return result
    for info in dwdb_list:
        i = {}
        for (k, v) in info.items():
            if k in dwdb_info_templ.keys():
                i.update({
                    dwdb_info_templ.get(k): v
                })
            else:
                logging.error("not have k in templ in dwdb_list  ...k:%s" % k)
                exit(-1)
        result.append(i)
    return result


xg_info_templ = {
    u"zqr": u"xh",  # 序号
    u"zwr": u"xgsx",
    u"zzqzl": u"xgq",
    u"zzqse": u"xgh",
    u"lxzwdqx": u"xgrq",
}


def parse_xg_list(xg_list):
    result = []
    if not xg_list:
        return result
    for info in xg_list:
        i = {}
        for (k, v) in info.items():
            if k in xg_info_templ.keys():
                i.update({
                    xg_info_templ.get(k): v
                })
            else:
                logging.error("not have k in templ in xg_list  ...k:%s" % k)
                exit(-1)
        result.append(i)
    return result


dwtz_info_templ = {
    u"name": u"companyName",
    u"code": u"registerNum"
}


def parse_dwtz_list(dwtz_list):
    result = []
    if not dwtz_list:
        return result
    for info in dwtz_list:
        i = {}
        for (k, v) in info.items():
            if k in dwtz_info_templ.keys():
                i.update({
                    dwtz_info_templ.get(k): v
                })
            else:
                logging.error("not have k in templ in dwtz_info_templ  ...k:%s" % k)
                exit(-1)
        result.append(i)
    return result


gdbg_info_templ = {
    u"gd": u"gd",  # 股东
    u"bgqbl": u"bgqbl",  # 变更前股权比例
    u"bghbl": u"bghbl",  # 变更后股权比例
    u"bgrq": u"bgrq",  # 股权变更日期
}


def parse_gdbg_list(gdbg_list):
    result = []
    if not gdbg_list:
        return result
    for info in gdbg_list:
        i = {}
        for (k, v) in info.items():
            if k in gdbg_info_templ.keys():
                i.update({
                    gdbg_info_templ.get(k): v
                })
            else:
                logging.error("not have k in templ in gdbg_list  ...k:%s" % k)
                exit(-1)
        result.append(i)
    return result


def push_zb(qynb_info, reg_bus_ent_id):
    if check_pushed(reg_bus_ent_id):
        logging.info("pass........")
        return

    # url = "https://data.api.zhironghao.com/update/qiyenianbao"
    url = "https://data.api.zhironghao.com/update/qiyenianbao"

    data = {}

    d = dict(qynb_info)

    data.update({
        u"updateTime": d.get("date"),
        u"year": d.get("year"),
    })

    # data.update({u"companyName": company_name})

    qynb_detail = d.get("qynb_detail")
    if not qynb_detail:
        logging.error("not found qynb_detail....%s" % reg_bus_ent_id)
        return

    data.update(parse_company_base_info(qynb_detail.get("base_info")))
    data.update(parse_qyzczk_info(qynb_detail.get("qyzczk_info")))

    data.update({
        # "companyBaseInfo": parse_company_base_info(qynb_detail.get("base_info")),
        # "qyzczkInfo": parse_qyzczk_info(qynb_detail.get("qyzczk_info")),
        u"gdczInfo": json.dumps(parse_gdcz_info_list(qynb_detail.get("gdcz_list"))),
        u"websiteInfo": json.dumps(parse_website_info_list(qynb_detail.get("wz_list"))),
        u"dwtgdbInfo": json.dumps(parse_dwdb_list(qynb_detail.get("dwdb_list"))),
        u"xgjlInfo": json.dumps(parse_xg_list(qynb_detail.get("xg_list"))),
        u"dwtzInfo": json.dumps(parse_dwtz_list(qynb_detail.get("dwtz_list"))),
        u"gdbgInfo": json.dumps(parse_gdbg_list(qynb_detail.get("gdbg_list"))),
    })

    company_name = data.get(u"companyName")

    if not company_name:
        logging.error("not found companyName, before push")
        return

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


def push_all():
    cur = qyxy_baic_db.company_info_detail_level_1.find().batch_size(50)

    # times = 20

    for level_1 in cur:

        reg_bus_ent_id = level_1.get("reg_bus_ent_id")

        # company = qyxy_baic_db.company_info.find_one({"reg_bus_ent_id": reg_bus_ent_id})
        # base_info = company.get("base_info")
        # if not base_info:
        #     logging.error("not found base info....%s" % reg_bus_ent_id)
        #     continue
        # gsdjzc_info = base_info.get("gsdjzc_info")
        # if not gsdjzc_info:
        #     logging.error("not found gsdjzc_info....%s" % reg_bus_ent_id)
        #     continue
        # company_name = gsdjzc_info.get(u"名称")

        gsgs_info = level_1.get("gsgs_info")
        if not gsgs_info:
            logging.error("not found gsgs_info....%s" % reg_bus_ent_id)
            continue

        qynb = gsgs_info.get("qynb")
        if not qynb:
            logging.error("not found qynb....%s" % reg_bus_ent_id)
            continue

        for qynb_info in qynb:
            push_zb(qynb_info, reg_bus_ent_id)

            # break  # 只push一次测
            # times -= 1
            # if times < 0:
            #     break


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
        init_logging(error_file="log/qynb/error.log", info_file="log/qynb/info.log",
                     noset_file="log/qynb/noset.log")
        push_all()
        # check_templ_all()
        logging.info("finish..........")
    except Exception, e:
        logging.exception(e)
