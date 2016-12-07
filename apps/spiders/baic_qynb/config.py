# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from apps.spiders.common.base_config import BaseConfig


class Config(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)

        host = "qyxy"
        host += "."
        host += "baic"
        host += "."
        host += "gov"
        host += "."
        host += "cn"

        self.host = host
        self.domain = "http://" + self.host

        self.search_key_collection_name = "baic"
