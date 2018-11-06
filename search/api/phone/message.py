# -*- coding:utf8 -*-
#pylint: disable=E1101,C0103
import datetime

from flask import g, current_app
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from sqlalchemy import func

from search import db
from search.swagger import ResponseModel
from search.models import Users, Messages
from search.api.auth.utils import token_required

put_parser = reqparse.RequestParser()
put_parser.add_argument('messages', type=str, required=True, location='form')

get_parser = reqparse.RequestParser()
get_parser.add_argument('phone', type=str, required=True, location='args')

class Message(Resource):
    @swagger.doc({
        'tags': ['contact'],
        'description': '메시지 저장',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '토큰으로 유저 조회',
                'in': 'header',
                'type': 'string',
                'required': True
            }, {
                'name': '메시지 저장',
                'description': '데이터는 010-1234-1234|내용입니다만...|2018-10-20 23:12:11 이런식으로 구분자는 줄바꿈',
                'in': 'formData',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '메시지 저장 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '메시지 저장 성공'
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
    @token_required
    def put(self):
        """ 메시지 저장 """

        old_time = datetime.datetime.now()

        args = put_parser.parse_args()

        user = g.user.id
        
        message_list = args['messages'].split('\n')

        for i in range(len(message_list)):
            field = message_list[i].split('|')
            print(field[0])
            print(field[1])
            print(field[2])
            print(field[3])

            message = Messages()
            message.uid = user
            message.phone = field[0]
            message.content = field[1]
            message.type = field[2]
            message.created_at = field[3]

            db.session.add(message)

        db.session.commit()

        cur_time = datetime.datetime.now()

        print(cur_time - old_time)

        return {
            'code': 200,
            'message': '메시지 저장 성공.'
        }, 200

    @swagger.doc({
        'tags': ['contact'],
        'description': '메시지 조회',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '토큰으로 유저 조회',
                'in': 'header',
                'type': 'string',
                'required': True
            }, {
                'name': 'phone',
                'description': '010-1010-1010',
                'in': 'header',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '메시지 조회 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '메시지 조회 성공',
                        "data": {
                            "messages": [
                                {
                                    "id": 1,
                                    "uid": 1,
                                    "phone": "010-1234-1234",
                                    "content": "내용입니다만...",
                                    "created_at": "2018-10-20 23:12:11",
                                    "shop_name": "사용자입니다"
                                }
                            ]
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
    @token_required
    def get(self):
        """ 메시지 조회 """

        old_time = datetime.datetime.now()

        args = get_parser.parse_args()

        user = g.user.id

        search = Messages.query\
            .filter(Messages.phone == args['phone'])\
            .group_by(Messages.uid)\
            .order_by(Messages.created_at.desc())\
            .all()
        print(search)
        print(len(search))

        cur_time = datetime.datetime.now()

        print(cur_time - old_time)

        return {
            'code': 200,
            'message': '메시지 조회 성공.',
            'data': {
                'messages': [
                    x.get_message_object() for x in search
                ]
            }
        }, 200