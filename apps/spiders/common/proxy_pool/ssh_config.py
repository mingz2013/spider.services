# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

username = 'root'
password = 'aa0d0a4a9166'


def get_ssh_config(num):
    _config = [
        {"ip": '118.119.102.36', "port": 20363},
        {"ip": '113.59.34.55', "port": 20119},
        {"ip": '221.10.205.22', "port": 20611},
        {"ip": '221.10.101.119', "port": 20461},
        {"ip": '221.10.170.70', "port": 20381},
        {"ip": '221.10.137.9', "port": 20181}
    ]
    return _config[num]
