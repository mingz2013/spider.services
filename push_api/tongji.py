# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo
import logging

mongo_client = pymongo.MongoClient()

company_clean_db = mongo_client["company_clean"]

from log import init_logging

init_logging()

cur = company_clean_db.swdj_info_r.find()

r = {}

for item in cur:
    l = len(item.items())
    s_l = str(l)
    count = r.get(s_l)
    count = count + 1 if count else 1

    # logging.info("%s:%s" % (s_l, count))
    r.update({s_l: count})

logging.info(r)
