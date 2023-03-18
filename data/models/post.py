import sqlalchemy
from sqlalchemy import orm
from ..db_session import SqlAlchemyBase
from .association_tables import Likes


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True,
                           unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))

    is_text = sqlalchemy.Column(sqlalchemy.Boolean)
    text = sqlalchemy.Column(sqlalchemy.String)

    is_file = sqlalchemy.Column(sqlalchemy.Boolean)
    file_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('files.id'))

    date_time = sqlalchemy.Column(sqlalchemy.DateTime)

    # one to one
    chat = orm.relationship('CommentsChat', back_populates='post')

    # many to one
    file = orm.relationship('File')
    user = orm.relationship('User')

    # many to many
    likes = orm.relationship('User',
                             secondary=Likes,
                             back_populates='likes')

    def __repr__(self):
        return f'<Post> id: {self.id} author: {self.user}'
