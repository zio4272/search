# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from search import db

class CallLogs(db.Model):
    """ 통화기록 테이블 """
    __tablename__ = 'call_logs'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(40), nullable=False) # 저장된 이름
    log_type = db.Column(db.Enum('IN','OUT','MISS'), nullable=False) # 종류 : 수신, 발신, 부재중
    phone = db.Column(db.String(40), nullable=False) # 전번
    time = db.Column(db.String(40), nullable=False) # 통화시간 얼마나 했는지
    created_at = db.Column(db.String(40), nullable=False) # 전화를 한 시간

    user = db.relationship('Users')

    def get_call_log_object(self):
        call_log = {
            'id': self.id,
            'uid': self.uid,
            'name': self.name,
            'log_type': self.log_type,
            'phone': self.phone,
            'time': self.time,
            'created_at': self.created_at
        }
        call_log['shop_name'] = self.user.name

        return call_log