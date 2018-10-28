# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from search import db

class Contacts(db.Model):
    """ 연락처 테이블 """
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone = db.Column(db.String(40), nullable=False) # 전번
    name = db.Column(db.String(40), nullable=False) # 저장된 이름
    created_at = db.Column(db.String(40), nullable=False) #저장된 날짜

    user = db.relationship('Users')

    def get_contact_object(self):
        contact = {
            'id': self.id,
            'uid': self.uid,
            'phone': self.phone,
            'name': self.name,
            'created_at': self.created_at
        }
        contact['shop_name'] = self.user.name
        return contact