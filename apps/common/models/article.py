# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import time

from ..base0 import Base0
from ...utils.utils import require_value_from_dict


class Article(Base0):
    """
    文章
    """

    def __init__(self, obj):
        Base0.__init__(self)

        self.title = require_value_from_dict(obj, 'title')
        self.content = require_value_from_dict(obj, 'content')
        # self.summary = require_value_from_dict(obj, 'summary') # 摘要

        # self.user_id = require_value_from_dict(obj, 'user_id')
        self.author = require_value_from_dict(obj, 'author')

        self.create_time = time.time()
        # self.update_time = time.time()

        self.from_site = require_value_from_dict(obj, 'from_site')
        self.from_url = require_value_from_dict(obj, 'from_url')

        self.category = require_value_from_dict(obj, 'category')
        self.tags = require_value_from_dict(obj, 'tags')

        self.status = 0  # -1: 删除, 0: 草稿, 1:发布
        # self.publish_time = None

        self.view_times = 0
