# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from flask import Flask, render_template

# from flask.ext.bootstrap import Bootstrap
# from flask.ext.mail import Mail
# from flask.ext.moment import Moment
# from flask.ext.sqlalchemy import SQLAlchemy
from config import config_dict
import sys

import logging
from logging.handlers import RotatingFileHandler

# bootstrap = Bootstrap()
# mail = Mail()
# moment = Moment()
# db = SQLAlchemy()
# convert python's encoding to utf8
try:
    from imp import reload

    reload(sys)
    sys.setdefaultencoding('utf8')
except (AttributeError, NameError):
    print "set default coding utf-8 error"


def _import_submodules_from_package(package):
    import pkgutil

    modules = []
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix=package.__name__ + "."):
        if ispkg:
            modules.extend(_import_submodules_from_package(__import__(modname, fromlist="dummy")))
        else:
            modules.append(__import__(modname, fromlist="dummy"))
    return modules


def register_routes(app):
    from . import controllers
    from flask.blueprints import Blueprint

    for module in _import_submodules_from_package(controllers):
        if hasattr(module, 'api'):
            bp = getattr(module, 'api')
        else:
            app.logger.error('api not in module')

        if bp and isinstance(bp, Blueprint):
            app.register_blueprint(bp)
        else:
            app.logger.error('bp is not blusprint')

    @app.errorhandler(403)
    def page_403(error):
        app.logger.error("403")
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def error_404(error):
        app.logger.error("404")
        return render_template('errors/404.html'), 404


def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_mode])
    config_dict[config_mode].init_app(app)
    app.config_mode = config_mode

    # 内部日志
    rotating_handler1 = RotatingFileHandler('logs/info.log', maxBytes=1 * 1024 * 1024, backupCount=5)
    rotating_handler2 = RotatingFileHandler('logs/error.log', maxBytes=1 * 1024 * 1024, backupCount=2)
    formatter1 = logging.Formatter("-" * 100 +
                                   '\n %(asctime)s %(levelname)s - '
                                   'in %(funcName)s [%(filename)s:%(lineno)d]:\n %(message)s')
    rotating_handler1.setFormatter(formatter1)
    rotating_handler2.setFormatter(formatter1)
    app.logger.addHandler(rotating_handler1)
    app.logger.addHandler(rotating_handler2)
    app.logger.setLevel(logging.INFO)
    rotating_handler2.setLevel(logging.ERROR)
    if app.config.get("DEBUG"):
        # app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.DEBUG)

    # bootstrap.init_app(app)
    # mail.init_app(app)
    # moment.init_app(app)
    # db.init_app(app)
    register_routes(app)
    # 定时器
    # scheduler.init_app(app)
    # scheduler.start()
    # from apps.routes import main
    # app.register_blueprint(main)

    return app
