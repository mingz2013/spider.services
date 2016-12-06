# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from apps.spiders.common.default_config import DefaultConfig


class Config(DefaultConfig):
    def __init__(self):
        DefaultConfig.__init__(self)

        from haha import host
        host += "."
        host += "gov"
        host += "."
        host += "cn"

        self.host = host
        self.domain = "http://" + self.host
