import sqlalchemy
from sqlalchemy import orm
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

    # many to one
    user = orm.relationship('User')

    # one to many
    messages = orm.relationship('Message', back_populates='file')
    posts = orm.relationship('Post', back_populates='file')

    def get_file(self, mode='rb'):
        return open(self.path, mode=mode)

    def __repr__(self):
        return f'<File> id: {self.id} name: {self.name} path: {self.path}'

