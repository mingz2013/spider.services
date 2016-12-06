# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import time

from .base0 import Base0
from ..utils import require_value_from_dict


class Company(Base0):

    def __init__(self, obj):
        Base0.__init__(self)

        self.company_name = require_value_from_dict(obj, 'company_name')
