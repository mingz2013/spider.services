# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import math
import random
import time

import requests

from captcha import read_body_to_string
from config import domain, host

default_headers = {
    'Host': host,
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
    # 'Cookie': '',
}

session = requests.Session()
session.headers = default_headers
index_url = domain + '/simple/dealSimpleAction!transport_ww.dhtml'
print "index_url:->", index_url

# requests.utils.add_dict_to_cookiejar(session.cookies, {'CNZZDATA1257386840': ''})

response = session.get(index_url)
print session.cookies

from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, 'lxml')

currentTimeMillis = soup.select_one('input[id="currentTimeMillis"]')['value']
print "currentTimeMillis:->", currentTimeMillis

default_headers = {
    'Host': host,
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    'Accept': 'image/webp,image/*,*/*;q=0.8',
    'Referer': domain + '/simple/dealSimpleAction!transport_ww.dhtml',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
    # 'Cookie': '',
}
# default_headers.update({"Cookie": session.headers.get("Cookie")})
session.headers = default_headers

print session.headers
code_img_url = domain + "/CheckCodeYunSuan?currentTimeMillis=%s" % currentTimeMillis
print "code_img_url:->", code_img_url
response = session.get(code_img_url)
check_code = read_body_to_string(response.content)
print "check_code:->", check_code
time.sleep(5)

print session.cookies

default_headers = {
    'Host': host,
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Accept': 'text/plain, */*; q=0.01',
    'Origin': domain,
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    'Referer': domain + '/simple/dealSimpleAction!transport_ww.dhtml',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
    # 'Cookie': '',  这里的cookie,需要带上CNZZDATA1257386840=688252775-1475221733-%7C1475221733
}
# default_headers.update({"Cookie": "; " + session.headers.get("Cookie")})
session.headers = default_headers

verify_url = domain + "/login/loginAction!checkCode.dhtml?check_code=%s&currentTimeMillis=%s&random=%s" % (
    check_code, currentTimeMillis, int(math.ceil(random.random() * 100000)))
print "verify_url:->", verify_url
print session.headers
response = session.post(verify_url)

print session.cookies

print response.content



# http://s4.cnzz.com/z_stat.php?id=1257386840&web_id=1257386840
# http://s4.cnzz.com/z_stat.php?id=1257386840&web_id=1257386840
# 固定的
# 	/	2017-03-31T09:38:30.000Z	93
