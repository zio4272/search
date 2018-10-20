# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from search import db

class Users(db.Model):
    """ 사용자 테이블 """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), nullable=False, unique=True) #아이디는 폰번호로
    auth = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(11), nullable=False) # 이름
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now) # 가입일

    contact = db.relationship('Contacts')
    call_log = db.relationship('CallLogs')
    message = db.relationship('Messages')
    period = db.relationship('Periods')

    def get_user_object(self):
        user = {
            'id': self.id,
            'user_id': self.user_id,
            'auth': self.auth,
            'name': self.name,
            'created_at': self.created_at
        }

        return user