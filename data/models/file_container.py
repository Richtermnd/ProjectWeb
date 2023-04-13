import sqlalchemy
from sqlalchemy import orm

from ..db_session import SqlAlchemyBase, create_session
from .association_tables import FileToContainer

from flask import render_template

class FileContainer(SqlAlchemyBase):
    """ Contain list of files for posts, messages and another """
    __tablename__ = 'file_containers'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True,
                           unique=True)
    files = orm.relationship('File',
                             secondary=FileToContainer,
                             back_populates='containers', 
                             lazy='dynamic')
    

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
        return render_template('file_container.jinja', container=self)

