import sqlalchemy
from sqlalchemy import orm
from ..db_session import SqlAlchemyBase
from .association_tables import Likes, FileToContainer


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
    file_container_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('file_containers.id'))

    date_time = sqlalchemy.Column(sqlalchemy.DateTime)

    # one to one
    chat = orm.relationship('CommentsChat', back_populates='post')

    # many to one
    user = orm.relationship('User')
    file_container = orm.relationship('FileContainer')

    # many to many
    likes = orm.relationship('User',
                             secondary=Likes,
                             back_populates='likes')

    def __repr__(self):
        return f'<Post> id: {self.id} author: {self.user}'
