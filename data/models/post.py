import datetime
from flask import render_template
import sqlalchemy
from sqlalchemy import orm
from ..db_session import SqlAlchemyBase, create_session
from .association_tables import Likes, FileToContainer


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True,
                           unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey('users.id'))

    is_text = sqlalchemy.Column(sqlalchemy.Boolean)
    text = sqlalchemy.Column(sqlalchemy.String)

    is_file = sqlalchemy.Column(sqlalchemy.Boolean)
    file_container_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                          sqlalchemy.ForeignKey('file_containers.id'))
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey('comments_chats.id'))

    date_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    # one to one
    chat = orm.relationship('CommentsChat', back_populates='post')

    # many to one
    user = orm.relationship('User', lazy='joined')
    file_container = orm.relationship('FileContainer', lazy='joined')

    # many to many
    likes = orm.relationship('User',
                             secondary=Likes,
                             back_populates='likes')

    def __repr__(self):
        return f'<Post> id: {self.id} author: {self.user}'
    
    def render(self, **kwargs):
        with create_session() as session:
            attrs = ' '.join([f'{key}="{value}"' for key, value in kwargs.items()])
            return render_template('post.jinja', post=self)
