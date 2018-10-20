# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from search import db

class Periods(db.Model):
    """ 결제관련 테이블 """
    __tablename__ = 'periods'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start = db.Column(db.String(40), nullable=False) # 시작일
    end = db.Column(db.String(40), nullable=False) # 종료일
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now) # 생성날짜

    def get_period_object(self):
        period = {
            'id': self.id,
            'uid': self.uid,
            'start': self.start,
            'end': self.end,
            'created_at': self.created_at
        }

        return period