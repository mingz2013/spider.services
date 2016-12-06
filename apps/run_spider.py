# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

# from spider import Spider
from spiders.article.csdn.spider import Spider
# from config import userId, password
from commons.spider.log import init_logging

import sys
import time
import logging

reload(sys)
sys.setdefaultencoding("utf-8")
print "sys default encoding: ", sys.getdefaultencoding()


def main():
    init_logging()
    begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    spider = Spider()
    spider.run()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    logging.info("-------begin: %s, end: %s--------" % (begin_time, end_time))
    pass


if __name__ == "__main__":
    main()
    pass
