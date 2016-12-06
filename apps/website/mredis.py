# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import os

import redis

REDIS_HOST = os.getenv("REDIS_HOST", '127.0.0.1')
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)


# 向redis里缓存用户信息 key:user_info field:user_id value:name;head_img_url
# redis> HSET myhash field1 "Hello"
#
# USER_INFO_KEY = "user_info"
# USER_OPENID = "user_openid"
# TOKEN = "token"
# TOKEN_EXPIRE_SECONDS = 3600 * 24 * 90  # 三个月
# USER_ID = "user_id"
# CLUB_ID = "club_id"
# EVENT_ID = "event_id"
# POST_ID = "post_id"
# VENUE_ID = "venue_id"
# COMPANY_ID = "company_id"
# SMS_ID = 'sms_id'
# SMS_CODE = "sms_code"
# SMS_USER_TIMES = "sms_user_times"
# ROBOT_QQ_KEY = "robot_qq_key"
# ADMIN_TOKEN = "admin_token"
# EVENT_KEY = "event_key"

# redis_client.expire(EVENT_KEY, 30)
# redis_client.expire(ROBOT_QQ_KEY, 3)
# redis_client.expire(SMS_USER_TIMES, 3600 * 2)
# redis_client.expire(SMS_CODE, 300)
# redis_client.expire(TOKEN, TOKEN_EXPIRE_SECONDS)
# redis_client.expire(ADMIN_TOKEN, 60 * 60 * 24)


class RedisClient(object):
    def __init__(self):
        pass
