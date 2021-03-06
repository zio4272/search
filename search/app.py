# -*- coding:utf8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful_swagger_2 import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object('search.config.{0}'.format(config_name))

    db.init_app(app)

    api = Api(app, api_version='0.0', api_spec_url='/api/spec', title='search spec', catch_all_404s=True)

    from .api.auth import Auth
    from .api.admin import Admin
    from .api.phone import Contact, Message, CallLog
    from .api.popup import Popup
    from .api.period import Period
    from .api.notice import Notice
    
    api.add_resource(Auth, '/auth')

    api.add_resource(Admin, '/admin')

    api.add_resource(Contact, '/contact')
    api.add_resource(Message, '/message')
    api.add_resource(CallLog, '/call_log')

    api.add_resource(Popup, '/popup')
    
    api.add_resource(Period, '/period')

    api.add_resource(Notice, '/notice')

    swaggerui_blueprint = get_swaggerui_blueprint('/api/docs', '/api/spec.json', config={'app_name': 'search'})
    app.register_blueprint(swaggerui_blueprint, url_prefix='/api/docs')

    return app