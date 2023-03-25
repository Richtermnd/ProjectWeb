import datetime
import os

import sqlalchemy
from sqlalchemy import orm

from .association_tables import FileToContainer
from ..db_session import SqlAlchemyBase, create_session

from flask import url_for

class File(SqlAlchemyBase):
    __tablename__ = 'files'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True,
                           unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    path = sqlalchemy.Column(sqlalchemy.String)
    date_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    is_displayable = sqlalchemy.Column(sqlalchemy.Boolean)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    # many to one
    user = orm.relationship('User')

    containers = orm.relationship('FileContainer',
                                  secondary=FileToContainer,
                                  back_populates='files')
    

    def render(self, **kwargs):
        attrs = ' '.join([f'{key}="{value}"' for key, value in kwargs.items()])
        if self.is_displayable:
            return f"""<img src={self.url()} {attrs}>"""
        else:
            # Make alternative render for not displayable files
            return ''
    
    def url(self):
        return url_for('static', filename=self.path)

    def __enter__(self, mode='rb'):
        self.__pointer = open(self.path, mode=mode)
        return self.__pointer

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__pointer.close()

    def __repr__(self):
        return f'<File> id: {self.id} name: {self.name} path: {self.path}'
