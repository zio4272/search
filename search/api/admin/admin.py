# -*- coding:utf8 -*-
#pylint: disable=E1101,C0103
import datetime

from flask import g, current_app
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from sqlalchemy import func

from search import db
from search.swagger import ResponseModel
from search.models import Users, Periods, Admins
from search.api.auth.utils import token_required

post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', type=str, required=True, location='form')
post_parser.add_argument('name', type=str, required=True, location='form')
post_parser.add_argument('start_date', type=str, required=True, location='form')
post_parser.add_argument('end_date', type=str, required=True, location='form')

class Admin(Resource):
    @swagger.doc({
        'tags': ['admin'],
        'description': '회원 등업',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '토큰으로 유저 조회',
                'in': 'header',
                'type': 'string',
                'required': True
            }, {
                'name': 'user_id',
                'description': '회원전화번호 - 01012345678 형식으로 기재',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'name',
                'description': '업소명 - 지역업종-이름 형식으로 기재 ',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'start_date',
                'description': '시작일 - 2019-01-01 형식으로 기재',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'end_date',
                'description': '종료일 - 2019-03-01 형식으로 기재',
                'in': 'formData',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '회원 등업 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '회원 등업 성공'
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
    def post(self):
        """ 회원 등업 """
        args = post_parser.parse_args()

        user = g.user

        admin = Users.query\
            .filter(Users.id == Admins.uid)\
            .filter(Users.id == user.id)\
            .first()

        if admin:
            user = Users.query\
                .filter(Users.user_id == args['user_id'])\
                .first()
            
            if user:

                user.name = args['name']
                
                check = Periods.query\
                    .filter(Periods.uid == user.id)\
                    .first()
                print(check)
                
                # period에 없는 경우
                if not check:

                    period = Periods()
                    period.uid = user.id
                    period.start = args['start_date']
                    period.end = args['end_date']

                    db.session.add(period)
                    db.session.commit()

                # period에 있는 경우
                else:
                    check.end = args['end_date']
                    check.updated_at = datetime.datetime.now()

                    db.session.commit()
                            
                return {
                    'code': 200,
                    'message': '회원 등업 성공.'
                }, 200

            return {
                'code': 400,
                'message': '존재하지 않는 회원 입니다.'
            }, 400

        return {
            'code': 400,
            'message': '관리자가 아닙니다.'
        }, 400