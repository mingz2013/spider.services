# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import requests

if __name__ == "__main__":
    url = "http://localhost/api/push"

    payload = {
        "company_name": "123"
    }

    response = requests.post(url, data=payload)

    print response

    print response.content
