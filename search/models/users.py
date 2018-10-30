# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime
import re

from search import db

class Users(db.Model):
    """ 사용자 테이블 """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), nullable=False, unique=True) #아이디는 폰번호로
    auth = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(11)) # 이름
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now) # 가입일

    contact = db.relationship('Contacts')
    call_log = db.relationship('CallLogs')
    message = db.relationship('Messages')
    period = db.relationship('Periods', uselist=False)
    admin = db.relationship('Admins')

    def get_user_object(self, period_object=False, days_object=False):
        user = {
            'id': self.id,
            'user_id': self.user_id,
            'auth': self.auth,
            'name': self.name,
            'created_at': str(self.created_at)
        }

        if period_object:
            user['period'] = self.period.get_period_object() if self.period else None

        if days_object:

            end = datetime.datetime.strptime(self.period.end, "%Y-%m-%d")
            start = datetime.datetime.strptime(self.period.start, "%Y-%m-%d")

            value = (end - start)

            day = re.findall("\d+", str(value))
            
            user['days'] = day[0]

        return user