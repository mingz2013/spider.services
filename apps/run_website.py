# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from website import create_app

print "************* CURRENT CONFIG MODE: ", os.getenv('FOR_ADS')
mode = os.getenv('FOR_ADS') or 'default'
if mode:
    mode = mode.lower()
    print 'current config mode: %s' % mode
app = create_app(mode)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
