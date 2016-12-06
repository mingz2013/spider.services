# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from apps.common.mongo_db.company_collection import CompanyCollection


class APIService(object):
    def __init__(self):
        pass

    @staticmethod
    def insert_one(company):
        CompanyCollection.insert_one(company)
        pass
