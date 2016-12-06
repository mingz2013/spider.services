# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging
import sys
import time

from log import init_logging
from spider import Spider

reload(sys)
sys.setdefaultencoding("utf-8")
print "sys default encoding: ", sys.getdefaultencoding()


def main():
    init_logging("log/qianzhan_t3.log", "log/qianzhan_t3_2.log")
    spider = Spider(3)
    begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    spider.run(2)
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    logging.info("-------begin: %s, end: %s--------" % (begin_time, end_time))
    pass


# def thread_main():
#     init_logging("log/qianzhan.log", "log/qianzhan_2.log")
#
#     # data = [random.randint(1,10) for i in range(20)]
#     data_list = [0, 1]
#
#     pool = threadpool.ThreadPool(2)
#
#     requests = threadpool.makeRequests(thread_func, data_list)
#     [pool.putRequest(req) for req in requests]
#     pool.wait()
#
#     pass
#
#
# def thread_func(thread_id):
#
#     spider = Spider(thread_id)
#     begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#     spider.run(2)
#     end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#     logging.info("-------begin: %s, end: %s--------" % (begin_time, end_time))
#     pass


if __name__ == "__main__":
    main()
    # try:
    #     thread_main()
    # except Exception, e:
    #     logging.exception(e)
    # pass
