import sqlalchemy
from sqlalchemy import orm
from ..db_session import SqlAlchemyBase
from .association_tables import FileToContainer


class FileContainer(SqlAlchemyBase):
    """ Contain list of files for posts, messages and another """
    __tablename__ = 'file_containers'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True,
                           unique=True)
    files = orm.relationship('File',
                             secondary=FileToContainer)
