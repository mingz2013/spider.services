# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from flask import request, Blueprint, jsonify, current_app

from ..services.api_service import APIService
from common.models.company import Company

api = Blueprint('proxy_controller', __name__, url_prefix='/api')


@api.route('/test_ip', methods=['GET'])
def test_ip():
    current_app.logging.info("remote_addr: %s" % request.remote_addr)
    return request.remote_addr