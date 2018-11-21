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
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:dlstkrhk1q'+\
        '@phonebook.czyrqgd1z2hn.ap-northeast-2.rds.amazonaws.com/phone'

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
    