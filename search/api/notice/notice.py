# -*- coding:utf8 -*-
#pylint: disable=E1101,C0103
import datetime

from datetime import timedelta

from flask import g, current_app
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from sqlalchemy import and_

from search import db
from search.swagger import ResponseModel
from search.models import Users, Notices, Periods
from search.api.auth.utils import token_required, admin_required

put_parser = reqparse.RequestParser()
put_parser.add_argument('title', type=str, required=True, location='form')
put_parser.add_argument('content', type=str, required=True, location='form')

class Notice(Resource):
    @swagger.doc({
        'tags': ['notice'],
        'description': '공지사항 등록',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '토큰으로 유저 조회',
                'in': 'header',
                'type': 'string',
                'required': True
            }, {
                'name': 'title',
                'description': 'title',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'content',
                'description': 'content',
                'in': 'formData',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '공지사항 등록 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '공지사항 등록 성공',
                        "data": {
                            "notice": {
                                "id": 1,
                                "uid": 1,
                                "title": "제목입니다.",
                                "content": "내용입니다....람쥐",
                                "created_at": "2018-10-30 21:14:26"
                            }
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
    @admin_required
    def put(self):
        """ 공지사항 등록 """

        args = put_parser.parse_args()

        user = g.user

        if user:
            notice = Notices()
            notice.uid = user.id
            notice.title = args['title']
            notice.content = args['content']
            notice.created_at = datetime.datetime.now()

            db.session.add(notice)
            db.session.commit()

            return {
                'code': 200,
                'message': '공지사항 등록 성공.',
                'data': {
                    'notice': notice.get_notice_object()
                }
            }, 200

        return {
            'code': 400,
            'message': '관리자 계정이 아닙니다.'
        }, 400

    @swagger.doc({
        'tags': ['notice'],
        'description': '공지사항 조회',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '토큰으로 유저 조회',
                'in': 'header',
                'type': 'string',
                'required': True
            }, {
                'name': 'title',
                'description': 'title',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'content',
                'description': 'content',
                'in': 'formData',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '공지사항 조회 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '공지사항 조회 성공',
                        "data": {
                            "notice": [
                                {
                                    "id": 1,
                                    "uid": 1,
                                    "title": "제목입니다.",
                                    "content": "내용입니다....람쥐",
                                    "created_at": "2018-10-30 21:14:26"
                                },
                                {
                                    "id": 2,
                                    "uid": 1,
                                    "title": "두번째 공지사항.",
                                    "content": "내용이 들어감.",
                                    "created_at": "2018-10-30 21:40:34"
                                },
                                {
                                    "id": 3,
                                    "uid": 1,
                                    "title": "삼번",
                                    "content": "삼번~~",
                                    "created_at": "2018-10-30 21:41:02"
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
        """ 공지사항 조회 """

        user = g.user

        if user:
            notice = Notices.query.all()
            if notice:
                today = str(datetime.date.today())
                pay = Periods.query\
                    .filter(Periods.uid == user.id)\
                    .filter(and_(Periods.end >= today))\
                    .first()
                print(pay)
                if not pay:
                    return {
                        'code': 400,
                        'message': '목록을 볼 권한이 없는 회원입니다.'
                    }, 400

                return {
                    'code': 200,
                    'message': '공지사항 조회 성공.',
                    'data': {
                        'notice': [
                            x.get_notice_object() for x in notice
                        ]
                    }
                }, 200
            return {
                'code': 400,
                'message': '공지사항이 없습니다.'
            }, 400
