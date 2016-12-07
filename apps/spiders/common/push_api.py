# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import hashlib
import logging
import time

import requests

from config import default_key, default_u


def md5(data):
    m = hashlib.md5(data)
    return m.hexdigest()


def get_k(u, t, key):
    return md5(u + t + key)


def push_request(url, data):
    response = requests.post(url, data=data)
    # response = requests.get(url, params=payload)
    return response


def push_data(url, data):
    u = default_u
    t = int(time.time())
    key = default_key
    k = get_k(u, str(t), key)

    payload = data

    payload.update({
        "t": t,
        "u": u,
        "k": k,
    })
    logging.info(payload.get("companyName"))
    logging.debug(payload)
    return push_request(url, payload)


if __name__ == "__main__":
    from init_logging import init_logging

    init_logging()
    url = "https://data.api.zhironghao.com/update/gongshang"
    logging.debug(time.time())
    response = push_data(url, {u"companyName": u"123"})
    logging.info(response)
    logging.info(response.content)
