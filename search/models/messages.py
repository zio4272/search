# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from search import db

class Messages(db.Model):
    """ 메시지 테이블 """
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone = db.Column(db.String(40), nullable=False) # 전화번호 or 이름
    content = db.Column(db.Text, nullable=False) # 메시지 내용
    created_at = db.Column(db.String(40), nullable=False) # 날짜

    user = db.relationship('Users')

    def get_message_object(self):
        message = {
            'id': self.id,
            'uid': self.uid,
            'phone': self.phone,
            'content': self.content,
            'created_at': self.created_at
        }
        message['shop_name'] = self.user.name
        return message