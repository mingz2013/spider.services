# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging
import random

import pymongo

# MONGO
MONGO_URI = "localhost:27017"
mongo_client = pymongo.MongoClient(MONGO_URI)

qyxy_baic_db = mongo_client["qyxy_baic"]


# proxy_db = mongo_client['proxy']
# qianzhan_db = mongo_client['qianzhan']


class QyxybaicDB(object):
    def __init__(self):
        pass

    @staticmethod
    def upsert_company(company):
        logging.info("<MONGO> %s" % company)
        qyxy_baic_db.company_info.update({'reg_bus_ent_id': company['reg_bus_ent_id']}, {'$set': company}, True, True)

    @staticmethod
    def get_random_one_search_key_need():
        cur = qyxy_baic_db.search_key_need.find()
        count = cur.count()
        i = random.randint(0, count)
        return cur[i]

    @staticmethod
    def remove_search_key_from_need(search_key):
        qyxy_baic_db.search_key_need.remove({"search_key": search_key})

    @staticmethod
    def upsert_search_key_have(search_key):
        qyxy_baic_db.search_key_have.update({"search_key": search_key}, {"search_key": search_key}, True,
                                            True)

    @staticmethod
    def check_have(search_key):
        if qyxy_baic_db.search_key_have.find_one({"search_key": search_key}):
            return True
        else:
            return False

# class ProxyDB(object):
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def get_all():
#         return proxy_db.proxy_items_baic.find().batch_size(1)
#
#     @staticmethod
#     def remove_proxy(proxy_ip, proxy_port):
#         proxy_db.proxy_items_baic.remove({"ip": proxy_ip, "port": proxy_port})
#
#
# class QianzhanDB(object):
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def get_all_count():
#         return qianzhan_db.company_info_items_base.find({"province": "北京"}).count()
#
#     @staticmethod
#     def get_one(i):
#         return qianzhan_db.company_info_items_base.find({"province": "北京"}, {"company_name": 1}).skip(i).limit(1)
#
#     @staticmethod
#     def get_random_one():
#         cur = qianzhan_db.company_info_items_base.find()
#         count = cur.count()
#         i = random.randint(0, count)
#         return cur[i]
#
#
#     @staticmethod
#     def get_all():
#         return qianzhan_db.company_info_items_base.find({"province": "北京"}, {"company_name": 1}).batch_size(1)
#
#     @staticmethod
#     def upsert_company(item):
#         logging.info("<MONGO> %s" % item)
#         qianzhan_db.company_info_items_base.update({'company_name': item['company_name']}, {'$set': item}, True, True)
#
#     @staticmethod
#     def is_had(company_name):
#         cur = qianzhan_db.company_info_items_base.find_one({"company_name": company_name})
#         # logging.debug("cur:%s" % cur)
#         if cur:
#             return True
#         else:
#             return False
