# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from search import db

class CallLogs(db.Model):
    """ 통화기록 테이블 """
    __tablename__ = 'call_logs'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    log_type = db.Column(db.Enum('IN','OUT','MISS'), nullable=False) # 종류 : 수신, 발신, 부재중
    time = db.Column(db.String(40), nullable=False) # 통화시간 얼마나 했는지
    created_at = db.Column(db.String(40), nullable=False) # 전화를 한 시간

    def get_call_log_object(self):
        call_log = {
            'id': self.id,
            'uid': self.uid,
            'log_type': self.kind,
            'time': self.time,
            'created_at': self.created_at
        }

        return call_log