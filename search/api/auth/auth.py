# -*- coding:utf8 -*-
#pylint: disable=E1101,C0103
import datetime
import random

from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from search import db
from search.swagger import ResponseModel
from search.models import Users, Admins
from .utils import encode_token, decode_token, token_required

signup_parser = reqparse.RequestParser()
signup_parser.add_argument('user_id', type=str, required=True, location='form')

signin_parser = reqparse.RequestParser()
signin_parser.add_argument('user_id', type=str, required=True, location='form')
signin_parser.add_argument('auth', type=str, required=True, location='form')

token_parser = reqparse.RequestParser()
token_parser.add_argument('X-Http-Token', type=str, location='headers', dest='token')


class Auth(Resource):
    @swagger.doc({
        'tags': ['auth'],
        'description': '자동 회원가입',
        'parameters': [
            {
                'name': 'user_id',
                'description': '사용자 아이디 : 해당 기기의 번호를 받아옴',
                'in': 'formData',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '회원가입 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '회원가입 성공',
                        "data": {
                            "user": {
                                "id": 1,
                                "user_id": "010-1010-1010",
                                "auth": "50310635",
                                "name": "",
                                "created_at": "2018-10-20 20:50:15"
                            },
                            "token": "token"
                        }
                    }
                }
            },
            '400': {
                'description': '파라미터 값 이상',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 400,
                        'message': '특정 파라미터 값이 올바르지 않습니다.'
                    }
                }
            }
        }
    })
    def put(self):
        """ 회원가입 """
        args = signup_parser.parse_args()

        random_value = str(random.randrange(0,99999999))
      
        user = Users.query.filter_by(user_id=args['user_id']).first()
        if user is not None:
            return {
                'code': 400,
                'message': '중복된 사용자 전화번호가 있습니다.'
            }, 400

        user = Users.query.filter_by(auth=random_value).first()
        if user is not None:
            return {
                'code': 400,
                'message': '중복된 인증번호가 존재합니다.'
            }, 400

        new_user = Users()
        new_user.user_id = args['user_id']
        new_user.auth = random_value
        new_user.name = ''
        new_user.created_at = datetime.datetime.now()

        db.session.add(new_user)
        db.session.commit()     

        return {
            'code': 200,
            'message': '회원가입 성공입니다.',
            'data': {
                'user': new_user.get_user_object(),
                'token': encode_token(new_user)
            }
        }, 200
    
    @swagger.doc({
        'tags': ['auth'],
        'description': '인증 로그인',
        'parameters': [
            {
                'name': 'user_id',
                'description': '사용자 아이디 : 해당 기기의 번호를 받아옴',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'auth',
                'description': '사용자에 해당하는 auth 인증번호',
                'in': 'formData',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '인증 로그인',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '인증 로그인',
                        "data": {
                            "user": {
                                "id": 1,
                                "user_id": "010-1010-1010",
                                "auth": "50310635",
                                "name": "",
                                "created_at": "2018-10-20 20:50:15"
                            },
                            "token": "token"
                        }
                    }
                }
            },
            '400': {
                'description': '파라미터 값 이상',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 400,
                        'message': '특정 파라미터 값이 올바르지 않습니다.'
                    }
                }
            }
        }
    })
    def post(self):
        """ 인증 로그인 """
        args = signin_parser.parse_args()

        user = Users.query\
            .filter(Users.user_id == args['user_id'])\
            .filter(Users.auth == args['auth'])\
            .first()
        print(user)

        if not user:
            return {
                'code': 400,
                'message': '인증실패. 인증정보를 확인 해주세요.'
            }, 400

        return {
            'code': 200,
            'message': '인증 성공',
            'data': {
                'user': user.get_user_object(),
                'is_admin': True if user.admin else False,
                'token': encode_token(user)
            }
        }, 200

    @swagger.doc({
        'tags': ['auth'],
        'description': '토큰으로 유저 조회',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '토큰으로 유저 조회',
                'in': 'header',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '토큰으로 조회 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '토큰으로 조회 성공',
                        "data": {
                            "user": {
                                "id": 1,
                                "user_id": "010-1010-1010",
                                "auth": "50310635",
                                "name": "",
                                "created_at": "2018-10-20 20:50:15"
                            },
                            "token": "token"
                        }
                    }
                }
            },
            '400': {
                'description': '올바르지 않은 조회',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 400,
                        'message': '올바르지 않은 토큰입니다.'
                    }
                }
            }
        }
    })
    @token_required
    def get(self):
        """토큰으로 유저조회"""
        args = token_parser.parse_args()
        user = decode_token(args['token'])

        if user:
            return {
                'code': 200,
                'message': '토큰으로 유저조회 성공',
                'data': {
                    'user': user.get_user_object(period_object=True, days_object=True),
                    'token': encode_token(user)
                }
            }, 200
        return {
            'code': 400,
            'message': '올바르지 않은 토큰입니다.'
        }, 400,