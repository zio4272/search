# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from search import db

class Notices(db.Model):
    """ 공지사항 테이블 """
    __tablename__ = 'notices'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #작성자
    title = db.Column(db.String(40), nullable=False) # 제목
    content = db.Column(db.Text, nullable=False) # 내용
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now) # 생성날짜

    def get_notice_object(self):
        notice = {
            'id': self.id,
            'uid': self.uid,
            'title': self.title,
            'content': self.content,
            'created_at': str(self.created_at)
        }

        return notice