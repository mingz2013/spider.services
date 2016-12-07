# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import json
import logging

from push_api import push_data


class BasePush(object):
    def __init__(self):
        self._pass_list = self.get_pass_list()
        self._templ = self.get_templ()
        self._url = self.get_url()
        pass

    def get_pass_list(self):
        assert False, "need to be overwrite"
        return []

    def get_templ(self):
        assert False, "need to be overwrite"
        return {}

    def get_url(self):
        assert False, "need to be overwrite"
        return ""

    def push_info(self, info, company_name):
        data = {}

        d = dict(info)

        for (k, v) in d.items():
            if k in self._pass_list:
                continue
            is_have = False
            for (kk, vv) in self._templ.items():
                if k in vv:
                    if data.get(kk):
                        logging.error(u"repeat key, %s" % kk)
                        logging.error(d)
                        exit(-1)
                    data.update({kk: v})
                    is_have = True
                    break
            if not is_have:
                logging.error(u"unknown key, %s" % k)
                logging.error(d)
                exit(-1)

        data.update({u"companyName": company_name})

        response = push_data(self._url, data)
        if response.status_code != 200:
            logging.error("error status code: %s" % response.status_code)
            logging.error(d)
            # exit(-1)
            return
        try:
            r = json.loads(response.content)
            returnCode = r.get('returnCode')
            if returnCode == 0:
                logging.info("success.........")
            else:
                logging.error(r)
                # exit(-1)
        except Exception, e:
            logging.exception(e)
