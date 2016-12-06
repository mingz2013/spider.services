# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from apps.common.mongo_db.mongo_client_db import mongo_client_db


class GetSearchKey(object):
    def __init__(self, collection):
        self._collection = collection
        pass

    def get_search_key(self):
        item = mongo_client_db[self._collection].find_one()
        return item["company_name"]

    def remove_search_key(self, company_name):
        mongo_client_db[self._collection].remove({"company_name": company_name})
