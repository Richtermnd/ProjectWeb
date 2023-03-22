import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase

UserToChat = sqlalchemy.Table(
    'user_to_chat',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), primary_key=True),
    sqlalchemy.Column('chat', sqlalchemy.Integer, sqlalchemy.ForeignKey('chats.id'), primary_key=True),
)

Likes = sqlalchemy.Table(
    'likes',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), primary_key=True),
    sqlalchemy.Column('post', sqlalchemy.Integer, sqlalchemy.ForeignKey('posts.id'), primary_key=True),
    sqlalchemy.Column('date_time', sqlalchemy.DateTime, default=datetime.datetime.now())
)

Friends = sqlalchemy.Table(
    'friends',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user1', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), primary_key=True),
    sqlalchemy.Column('user2', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), primary_key=True)
)


FileToContainer = sqlalchemy.Table(
    'file_to_container',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('container', sqlalchemy.Integer, sqlalchemy.ForeignKey('file_containers.id'), primary_key=True),
    sqlalchemy.Column('file', sqlalchemy.Integer, sqlalchemy.ForeignKey('files.id'), primary_key=True)
)


