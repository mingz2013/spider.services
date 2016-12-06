# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from flask import request, Blueprint, jsonify, current_app

from ....services.api.user_api_service import UserAPIService
from commons.models.user.user import User

api = Blueprint('api_controller', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def index():
    return "user index"


@api.route('/', methods=['POST'])
def login():
    try:
        user = User(request.form)
        result = UserAPIService.login(user)
        return jsonify({'retcode': 0, 'errmsg': "", 'result': result})
    except Exception, e:
        return jsonify({'retcode': -1, 'errmsg': e.message, 'result': ""})
