# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from flask import request, Blueprint, jsonify, current_app

from ..services.api_service import APIService
from apps.common.models.company import Company

api = Blueprint('api_controller', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def index():
    return "api index"


@api.route('/push_one', methods=['POST'])
def push_one():
    try:
        company = Company(request.form)
        result = APIService.insert_one(company)
        return jsonify({'retcode': 0, 'errmsg': "", 'result': result})
    except Exception, e:
        return jsonify({'retcode': -1, 'errmsg': e.message, 'result': ""})
