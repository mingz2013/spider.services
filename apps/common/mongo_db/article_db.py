# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from bson import ObjectId

from ..mongo_client_db import mongo_client_db
from ...utils.utils import model2dict


class ArticleDB(object):
    def __init__(self):
        pass

    @staticmethod
    def get_article_list():
        article_list = mongo_client_db.articles.find()
        return article_list

    @staticmethod
    def get_article_list_by_category(category):
        article_list = mongo_client_db.articles.find({"category": category})
        return article_list

    @staticmethod
    def get_article_list_by_tag(tag):
        article_list = mongo_client_db.articles.find({"tags": tag})
        return article_list

    @staticmethod
    def get_article_list_by_month(month):
        article_list = mongo_client_db.articles.find({"month": month})
        return article_list

    @staticmethod
    def get_article_by_id(article_id):
        article = mongo_client_db.articles.find_one({"_id": ObjectId(article_id)})
        return article

    @staticmethod
    def remove_article_by_id(article_id):
        mongo_client_db.articles.remove({"_id": ObjectId(article_id)})

    @staticmethod
    def add_article(article):
        article_id = mongo_client_db.articles.insert(model2dict(article))
        return article_id

    @staticmethod
    def update_article(article):
        mongo_client_db.articles.update({"_id": ObjectId(article._id)}, model2dict(article))
