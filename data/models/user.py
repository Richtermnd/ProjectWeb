import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from ..db_session import SqlAlchemyBase
from .association_tables import Friends, Likes, UserToChat

from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    # model fields
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True,
                           unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    login = sqlalchemy.Column(sqlalchemy.String, default=id, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    birthdate = sqlalchemy.Column(sqlalchemy.Date)

    # one to many
    messages = orm.relationship('Message', back_populates='user')
    files = orm.relationship('File', back_populates='user')
    posts = orm.relationship('Post', back_populates='user')

    # many to many
    chats = orm.relationship('Chat',
                             secondary=UserToChat,
                             back_populates='users')
    likes = orm.relationship('Post',
                             secondary=Likes,
                             back_populates='likes')
    friends = orm.relationship('User',
                               secondary=Friends,
                               primaryjoin=id == Friends.c.user1,
                               secondaryjoin=id == Friends.c.user2)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, value):
        self.hashed_password = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<User> id: {self.id} name: {self.name}'
