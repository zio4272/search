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

put_parser = reqparse.RequestParser()
put_parser.add_argument('contacts', type=str, required=True, location='form')

get_parser = reqparse.RequestParser()
get_parser.add_argument('phone', type=str, required=True, location='args')

post_parser = reqparse.RequestParser()
post_parser.add_argument('phone', type=str, required=True, location='form')

class Contact(Resource):
    @swagger.doc({
        'tags': ['contact'],
        'description': '연락처 저장',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '토큰으로 유저 조회',
                'in': 'header',
                'type': 'string',
                'required': True
            }, {
                'name': 'contacts',
                'description': '데이터는 김|010-0000-0000|2010-10-10 11:11:11 이런식으로 구분자는 줄바꿈',
                'in': 'formData',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '연락처 저장 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '연락처 저장 성공'
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
        """ 연락처 저장 """

        old_time = datetime.datetime.now()

        args = put_parser.parse_args()

        user = g.user.id
        
        contact_list = args['contacts'].split('\n')

        for i in range(len(contact_list)):
            field = contact_list[i].split('|')
            # print(field[0])
            # print(field[1])
            # print(field[2])

            contact = Contacts()
            contact.uid = user
            contact.name = field[0]
            contact.phone = field[1]
            contact.created_at = field[2]

            db.session.add(contact)

        db.session.commit()

        cur_time = datetime.datetime.now()

        print(cur_time - old_time)

        return {
            'code': 200,
            'message': '연락처 저장 성공.'
        }, 200

    @swagger.doc({
        'tags': ['contact'],
        'description': '연락처 조회',
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
                'description': '연락처 조회 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '연락처 조회 성공',
                        "data": {
                            "contacts": [
                                {
                                    "id": 3290,
                                    "uid": 1,
                                    "phone": "010-1111-0000",
                                    "name": "김",
                                    "created_at": "2010-10-10 11:11:11",
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
        """ 연락처 조회 """

        old_time = datetime.datetime.now()

        args = get_parser.parse_args()

        user = g.user.id

        search = Contacts.query\
            .filter(Contacts.phone == args['phone'])\
            .all()

        cur_time = datetime.datetime.now()

        print(cur_time - old_time)

        return {
            'code': 200,
            'message': '연락처 조회 성공.',
            'data': {
                'contacts': [
                    x.get_contact_object() for x in search
                ]
            }
        }, 200