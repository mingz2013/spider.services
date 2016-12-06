# # -*- coding:utf-8 -*-
# __author__ = 'zhaojm'
#
# from mongo import QyxybaicDB
# import time
# import logging
# import random
#
#
# class GetSearchKey(object):
#     def __init__(self):
#         # self._search_key_cur = None
#         # self.refresh_search_key()
#         pass
#
#     # def refresh_search_key(self):
#     #     self._search_key_cur = QianzhanDB.get_all()
#     #     if self._search_key_cur.count() == 0:
#     #         logging.info("search_key is empty, sleep 30 * 60s")
#     #         time.sleep(30 * 60)
#
#     def get_search_key(self):
#         # try:
#         #     item = self._search_key_cur[random.randint(self._search_key_cur.count())]
#         #     return item['company_name']
#         # except Exception, e:
#         #     self.refresh_search_key()
#         #     return self.get_search_key()
#         # i = random.randint(1, 100000)
#         # item = QianzhanDB.get_one(i)[0]
#
