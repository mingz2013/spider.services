# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo
import logging
import random

# MONGO
# MONGO_URI = "localhost:27017"
# mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_client = pymongo.MongoClient()
job_58_db = mongo_client["job_58"]


class Job58DB(object):
    def __init__(self):
        pass

    # @staticmethod
    # def upsert_company(item):
    #     logging.info("<MONGO> %s" % item)
    #     job_58_db.company_info.update({'company_url': item['company_url']}, {'$set': item}, True, True)
    #
    # @staticmethod
    # def check_have(company_url):
    #     if job_58_db.company_info.find_one({"company_url": company_url}):
    #         return True
    #     else:
    #         return False

    # @staticmethod
    # def get_one_random_company_id():
    #     cur = job_58_db.company_info.find()
    #     count = cur.count()
    #     r = random.randint(count)
    #     company = cur[r]
    #     return company['company_id']

    # @staticmethod
    # def check_have_job(url):
    #     if job_58_db.job_info.find_one({"url": url}):
    #         return True
    #     else:
    #         return False

    @staticmethod
    def upsert_job(item):
        logging.info("<MONGO> %s" % item)
        job_58_db.job_info.update({'job_url': item['job_url']}, {'$set': item}, True, True)
