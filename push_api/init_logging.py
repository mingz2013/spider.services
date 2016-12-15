# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import logging
from logging.handlers import RotatingFileHandler


# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET

def init_logging(error_file="log/error.log", info_file="log/info.log", noset_file="log/noset.log"):
    format_str = '%(asctime)s %(filename)s[line:%(lineno)d] <%(levelname)s> %(message)s'

    formatter = logging.Formatter(format_str)

    logging.basicConfig(
        level=logging.NOTSET,
        format=format_str,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=noset_file,
        filemode='w',
    )

    # logging.basicConfig()
    # logging.getLogger().setLevel(logging.NOTSET)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
    Rthandler = RotatingFileHandler(info_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    Rthandler.setLevel(logging.INFO)
    Rthandler.setFormatter(formatter)
    logging.getLogger().addHandler(Rthandler)

    # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
    Rthandler1 = RotatingFileHandler(error_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    Rthandler1.setLevel(logging.ERROR)
    Rthandler1.setFormatter(formatter)
    logging.getLogger().addHandler(Rthandler1)


if __name__ == "__main__":
    init_logging()
    logging.debug('This is debug message')
    logging.info('This is info message')
    logging.warning('This is warning message')
    logging.error('This is error message')
    logging.critical('This is critical message')
