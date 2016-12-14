# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from apps.common.mongo_db.company_collection import CompanyCollection
from flask import current_app

class APIService(object):
    def __init__(self):
        pass

    @staticmethod
    def insert_one(company):
        ret = CompanyCollection.insert_one(company)
        current_app.logger.info(ret)
        return ""
