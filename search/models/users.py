# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from search import db

class Users(db.Model):
    """ 사용자 테이블 """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    area = db.Column(db.String(11), nullable=False) # 지역
    kind = db.Column(db.String(11), nullable=False) # 종류
    name = db.Column(db.String(11), nullable=False) # 이름
    phone = db.Column(db.String(20), nullable=False) # 전번
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now) # 가입일

    # company = db.relationship('Company')
    # password = db.Column(db.Integer, db.ForeignKey('area_main.am_idx'), nullable=False, default=0)

    contact = db.relationship('Contacts')

    def get_user_object(self):
        user = {
            'id': self.id,
            'user_id': self.user_id,
            'area': self.area,
            'kind': self.kind,
            'name': self.name,
            'phone': self.phone,
            'created_at': self.created_at
        }

        return user