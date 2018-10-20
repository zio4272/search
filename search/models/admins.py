# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from search import db

class Admins(db.Model):
    """ 관리자 테이블 """
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def get_admin_object(self):
        admin = {
            'id': self.id,
            'uid': self.uid,
            'created_at': self.created_at
        }

        return admin