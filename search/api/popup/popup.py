# -*- coding:utf8 -*-
#pylint: disable=E1101,C0103
import datetime

from flask import g, current_app
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from search import db
from search.swagger import ResponseModel
from search.models import Users, Contacts
from search.api.auth.utils import token_required

get_parser = reqparse.RequestParser()
get_parser.add_argument('phone', type=str, required=True, location='args')

class Popup(Resource):
    @swagger.doc({
        'tags': ['popup'],
        'description': '팝업 번호 조회',
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
                'description': '팝업 번호 조회 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '팝업 번호 조회 성공',
                        "data": {
                            "name": "이름",
                            "phone": "01012345678",
                            "total": "3"
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
        """ 팝업 번호 조회 """

        args = get_parser.parse_args()

        user = g.user.id

        search = Contacts.query\
            .filter(Contacts.phone == args['phone'])\
            .all()

        print(search)

        if search:
            total = 0
            for x in range(len(search)):
                total = x + 1

            return {
                'code': 200,
                'message': '팝업 번호 조회 성공.',
                'data': {
                    'name': search[0].name,
                    'phone': args['phone'],
                    'total' : str(total)
                } 
            }, 200
            
        return {
            'code': 400,
            'message': '결과 없음'
        }, 400