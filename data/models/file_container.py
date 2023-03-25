import sqlalchemy
from sqlalchemy import orm

from ..db_session import SqlAlchemyBase
from .association_tables import FileToContainer

from flask import render_template, url_for


class FileContainer(SqlAlchemyBase):
    """ Contain list of files for posts, messages and another """
    __tablename__ = 'file_containers'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True,
                           unique=True)
    files = orm.relationship('File',
                             secondary=FileToContainer,
                             lazy='joined')
    

    def __len__(self):
        return len(self.files)
    
    def displayable_files(self):
        res = []
        for file in self.files:
            if file.is_displayable:
                res.append(file)
        return res
    
    def render(self, **kwargs):
        attrs = ' '.join([f'{key}="{value}"' for key, value in kwargs.items()])
        return render_template('alt_file_container.jinja', container=self)

