# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from bson import ObjectId

from .mongo_client_db import mongo_client_db
from ..utils import model2dict

company_collection = mongo_client_db.company


class CompanyCollection(object):
    def __init__(self):
        pass

    @staticmethod
    def insert_one(company):
        company_collection.insert(model2dict(company))
