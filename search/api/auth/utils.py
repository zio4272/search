# -*- coding:utf8 -*-
from functools import wraps
import jwt

from flask import current_app, g
from flask_restful import reqparse

from search.models import Users

token_parser = reqparse.RequestParser()
token_parser.add_argument('X-Http-Token', type=str, location='headers', dest='token')

def encode_token(user):
    if not isinstance(user, Users):
        raise ValueError('arg1 is not instance of Member')

    return jwt.encode({'id': user.id, 'user_id': user.user_id,\
        }, current_app.config['JWT_SECRET'], algorithm=current_app.config['JWT_ALGORITHM']).decode("utf-8")

def decode_token(token):
    if token:
        try:
            decoded = jwt.decode(token, current_app.config['JWT_SECRET'],\
                algorithms=[current_app.config['JWT_ALGORITHM']])

            user = Users.query.filter_by(id=decoded['id'], user_id=decoded['user_id']).first()
            return user
        except jwt.exceptions.DecodeError:
            pass

    return None

def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        args = token_parser.parse_args()
        user = decode_token(args['token'])

        if user:

            g.user = user
            return func(*args, **kwargs)

        return {
            'code': 404,
            'message': '올바르지 않은 토큰입니다.'
        }, 404

    return decorator

def token_check(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        args = token_parser.parse_args()
        user = decode_token(args['token'])

        g.user = None
        if user:
            g.user = user

        return func(*args, **kwargs)
        
        
            # return {
            #     'code': 400,
            #     'message': '비회원 입니다.'
            # }, 400

        return {
            'code': 404,
            'message': '올바르지 않은 토큰입니다.'
        }, 404

    return decorator

def admin_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if g.user.admin:
            return func(*args, **kwargs)

        return {
            'code': 401,
            'message': '관리자 계정이 아닙니다.'
        }
    return decorator