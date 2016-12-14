# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import requests
import logging


def test_api_push():
    url = "http://localhost/push"
    data = {"company_name": "百度"}
    response = requests.post(url, data)
    logging.info(response)
    logging.info(response.content)
    pass


if __name__ == "__main__":
    test_api_push()
