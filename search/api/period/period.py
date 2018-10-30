# -*- coding:utf8 -*-
#pylint: disable=E1101,C0103
import datetime
import re

from datetime import timedelta

from flask import g, current_app
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from search import db
from search.swagger import ResponseModel
from search.models import Users, Periods
from search.api.auth.utils import token_required, admin_required

put_parser = reqparse.RequestParser()
put_parser.add_argument('uid', type=str, required=True, location='form')
put_parser.add_argument('month', type=str, required=True, location='form')

class Period(Resource):
    @swagger.doc({
        'tags': ['period'],
        'description': '결제 추가',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '토큰으로 유저 조회',
                'in': 'header',
                'type': 'string',
                'required': True
            }, {
                'name': 'uid',
                'description': 'uid',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'month',
                'description': '개월수 (1/2/3 등등) , 1 = 30일 , 2 = 60일 , 3 = 90일 . 곱하기 30일',
                'in': 'formData',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '결제 추가 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '결제 추가 성공'
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
    @admin_required
    def put(self):
        """ 결제추가 """

        args = put_parser.parse_args()

        user = g.user

        member = Periods.query\
            .filter(Periods.uid == args['uid'])\
            .first()

        if user:
            period = Periods()
            if not member:
                # 처음 결제한 회원인 경우 새로 생성
                period.uid = args['uid']
                period.start = datetime.date.today()
                print(period.start)
                period.end = period.start + datetime.timedelta(days = int(args['month']) * 30)
                print(period.end)
                period.created_at = datetime.datetime.now()

                db.session.add(period)
                db.session.commit()

                return {
                    'code': 200,
                    'message': '결제 추가 성공.',
                    'data': {
                        'period': period.get_period_object()
                    }
                }, 200

            else:
                # 기존에 결제한적이 있는 회원은 수정으로 
                member.start = datetime.date.today()
                print(period.start)
                member.end = member.start + datetime.timedelta(days = int(args['month']) * 30)
                print(period.end)
                print(member.end - member.start)
                
                value = (member.end - member.start)
                day = re.findall("\d+", str(value))
                
                print(type(day))

                db.session.commit()

                return {
                    'code': 200,
                    'message': '결제 추가 성공.',
                    'data': {
                        'day': day[0],
                        'period': member.get_period_object()
                    }
                }, 200
