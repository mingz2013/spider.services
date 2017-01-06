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

from push_tzr_list import push_tzr_list
from push_tzr_history_list import push_tzr_history_list
from push_ztz_list import push_ztz_list
from push_zyry_list import push_zyry_list


def push_all():
    cur = qyxy_baic_db.company_info_detail_level_2.find().batch_size(50)

    # times = 20

    for level_2 in cur:
        try:

            reg_bus_ent_id = level_2.get("reg_bus_ent_id")

            company = qyxy_baic_db.company_info.find_one({"reg_bus_ent_id": reg_bus_ent_id})
            base_info = company.get("base_info")
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

            tzr_list = level_2.get("tzr_list")
            if tzr_list:
                push_tzr_list(tzr_list, reg_bus_ent_id, company_name)
            tzr_history_list = level_2.get("tzr_history_list")
            if tzr_history_list:
                push_tzr_history_list(tzr_history_list, reg_bus_ent_id, company_name)
            ztz_list = level_2.get("ztz_list")
            if ztz_list:
                push_ztz_list(ztz_list, reg_bus_ent_id, company_name)
            zyry_list = level_2.get("zyry_list")
            if zyry_list:
                push_zyry_list(zyry_list, reg_bus_ent_id, company_name)
            fzjg_list = level_2.get("fzjg_list")
            if fzjg_list:
                # push_fzjg_list(fzjg_list, reg_bus_ent_id, company_name)
                logging.info(fzjg_list)
                logging.error("found fzjg list....")
                exit(-1)

                # break
        except Exception, e:
            logging.exception(e)


if __name__ == "__main__":
    try:
        init_logging(error_file="log/level_2/error.log", info_file="log/level_2/info.log",
                     noset_file="log/level_2/noset.log")
        push_all()
        # check_templ_all()
        logging.info("finish..........")
    except Exception, e:
        logging.exception(e)
