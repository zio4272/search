# -*- coding:utf8 -*-
#pylint: disable=E1101,C0103
import datetime

from flask import g, current_app
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from search import db
from search.swagger import ResponseModel
from search.models import Users, CallLogs
from search.api.auth.utils import token_required

put_parser = reqparse.RequestParser()
put_parser.add_argument('call_logs', type=str, required=True, location='form')

get_parser = reqparse.RequestParser()
get_parser.add_argument('phone', type=str, required=True, location='args')

class CallLog(Resource):
    @swagger.doc({
        'tags': ['contact'],
        'description': '전화기록 저장',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '토큰으로 유저 조회',
                'in': 'header',
                'type': 'string',
                'required': True
            }, {
                'name': '전화기록 저장',
                'description': '데이터는 김|010-0000-0000|2010-10-10 11:11:11 이런식으로 구분자는 줄바꿈',
                'in': 'formData',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '전화기록 저장 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '전화기록 저장 성공'
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
        """ 전화기록 저장 """

        old_time = datetime.datetime.now()

        args = put_parser.parse_args()

        user = g.user.id
        
        call_log_list = args['call_logs'].split('\n')

        for i in range(len(call_log_list)):
            field = call_log_list[i].split('|')
            # print(field[0])
            # print(field[1])
            # print(field[2])
            # print(field[3])
            # print(field[4])

            call_log = CallLogs()
            call_log.uid = user
            call_log.name = field[0]
            if field[1] == '수신':
                call_log.log_type = 'IN'
            elif field[1] == '발신':
                call_log.log_type = 'OUT'
            elif field[1] == '부재중':
                call_log.log_type = 'MISS'
            call_log.phone = field[2]
            call_log.time = field[3]
            call_log.created_at = field[4]

            db.session.add(call_log)

        db.session.commit()

        cur_time = datetime.datetime.now()

        print(cur_time - old_time)

        return {
            'code': 200,
            'message': '전화기록 저장 성공.'
        }, 200

    @swagger.doc({
        'tags': ['contact'],
        'description': '전화기록 조회',
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
                'description': '전화기록 조회 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '전화기록 조회 성공',
                        "data": {
                            "messages": [
                                {
                                    "id": 1,
                                    "uid": 1,
                                    "name": "저장된이름",
                                    "log_type": "IN",
                                    "phone": "010-1111-1111",
                                    "time": "00:04:11",
                                    "created_at": "2018-01-01 00:00:00",
                                    "shop_name": "사용자입니다"
                                },
                                {
                                    "id": 2,
                                    "uid": 1,
                                    "name": "저장된이름",
                                    "log_type": "OUT",
                                    "phone": "010-1111-1111",
                                    "time": "00:04:11",
                                    "created_at": "2018-01-01 00:00:00",
                                    "shop_name": "사용자입니다"
                                },
                                {
                                    "id": 3,
                                    "uid": 1,
                                    "name": "저장된이름",
                                    "log_type": "MISS",
                                    "phone": "010-1111-1111",
                                    "time": "00:04:11",
                                    "created_at": "2018-01-01 00:00:00",
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
        """ 전화기록 조회 """

        old_time = datetime.datetime.now()

        args = get_parser.parse_args()

        user = g.user.id

        search = CallLogs.query\
            .filter(CallLogs.phone == args['phone'])\
            .all()

        cur_time = datetime.datetime.now()

        print(cur_time - old_time)

        return {
            'code': 200,
            'message': '전화기록 조회 성공.',
            'data': {
                'call_logs': [
                    x.get_call_log_object() for x in search
                ]
            }
        }, 200