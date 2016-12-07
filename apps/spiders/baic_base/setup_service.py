# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging
import time

if __name__ == "__main__":
    from apps.spiders.common.init_logging import init_logging
    init_logging()
    from apps.common.default_encoding import init_encoding

    init_encoding()
    try:
        from config import Config

        c = Config()

        from spider import Spider

        spider = Spider(c)

        begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        spider.run()
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        logging.info("-------begin: %s, end: %s--------" % (begin_time, end_time))
    except Exception, e:
        logging.exception(e)
