# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from flask import request, Blueprint, jsonify, current_app, render_template

from ..services.api_service import APIService
from apps.common.models.company import Company

api = Blueprint('api_controller', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@api.route('/push', methods=['POST'])
def push():
    current_app.logger.info("request.form: %s" % request.form)
    try:
        company = Company(request.form)
        result = APIService.insert_one(company)
        return jsonify({'retcode': 0, 'errmsg': "", 'result': result})
    except Exception, e:
        current_app.logger.error(e.message)
        return jsonify({'retcode': -1, 'errmsg': e.message, 'result': ""})
