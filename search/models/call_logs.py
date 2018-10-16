# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from search import db

class CallLogs(db.Model):
    """ 통화기록 테이블 """
    __tablename__ = 'call_logs'

    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    time = db.Column(db.String(40), nullable=False) # 전화한 시간
    kind = db.Column(db.String(11), nullable=False) # 종류 : 발신, 수신, 부재중
    time2 = db.Column(db.String(40), nullable=False) # 통화시간

    def get_call_log_object(self):
        call_log = {
            'id': self.id,
            'cid': self.cid,
            'time': self.time,
            'kind': self.kind,
            'time2': self.time2
        }

        return call_log