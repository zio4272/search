# -*- coding:utf8 -*-
# pylint: disable=R0903
"""
Flask Configuration
"""

class Config(object):
    """
    Default Config Class for abstracting
    """
    DEBUG = False
    TESTING = False
    JWT_SECRET = 'some secret key'
    JWT_ALGORITHM = 'HS512'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:dlstkrhk1q'+\
        '@localhost/search'

class ProductionConfig(Config):
    """
    Production Config
    """
    pass

class TestConfig(Config):
    """
    Testing Config
    """
    TESTING = True

class DevelopmentConfig(Config):
    """
    For Development Config
    """
    DEBUG = True
    JWT_SECRET = 'some secret key'
    JWT_ALGORITHM = 'HS512'
    