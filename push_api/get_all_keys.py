# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import pymongo
import logging

mongo_client = pymongo.MongoClient()

_db = mongo_client["baidubaike"]

from init_logging import init_logging

init_logging()

cur = _db.company_info.find()

logging.info("..............begin................")
keys = []
for item in cur:
    keys.extend(item.keys())
keys.sort()

logging.info(len(keys))

d = {}
for key in keys:
    count = d.get(key)
    count = count if count else 0
    count += 1
    d.update({key: count})

logging.info(d)

keys = set(keys)
logging.info(keys)

logging.info("...........end...........................")
