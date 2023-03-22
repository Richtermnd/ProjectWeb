import sqlalchemy
from sqlalchemy import orm

from .association_tables import FileToContainer
from ..db_session import SqlAlchemyBase


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
    date_time = sqlalchemy.Column(sqlalchemy.DateTime)

    is_displayable = sqlalchemy.Column(sqlalchemy.Boolean)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean)

    # many to one
    user = orm.relationship('User')

    containers = orm.relationship('FileContainer',
                                  secondary=FileToContainer,
                                  back_populates='files')

    # non model attrs
    __pointer = None

    def __enter__(self, mode='rb'):
        self.__pointer = open(self.path, mode=mode)
        return self.__pointer

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__pointer.close()

    def __repr__(self):
        return f'<File> id: {self.id} name: {self.name} path: {self.path}'

