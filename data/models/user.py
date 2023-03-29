from flask import url_for
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from ..db_session import SqlAlchemyBase, create_session
from .association_tables import Friends, Likes, UserToChat, Avatars
from .file import File

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
    user_login = sqlalchemy.Column(sqlalchemy.String, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    birthdate = sqlalchemy.Column(sqlalchemy.Date)

    # optional info
    about = sqlalchemy.Column(sqlalchemy.String)
    contact_email = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    avatar = orm.relationship('File', secondary=Avatars)  # default avatar

    # one to many
    messages = orm.relationship('Message', back_populates='user')
    files = orm.relationship('File', back_populates='user')
    posts = orm.relationship('Post', 
                             back_populates='user',
                             lazy='selectin')

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
                               secondaryjoin=id == Friends.c.user2,
                               lazy='selectin')
    
    def form_data(self):
        data = {
            'name': self.name,
            'surname': self.surname,
            'user_login': self.user_login,
            'email': self.email,
            'birthdate': self.birthdate,
            'about': self.about,
            'contact_email': self.contact_email
        }
        return data
    
    def get_avatar(self, **kwargs):
        attrs = ' '.join([f'{key}="{value}"' for key, value in kwargs.items()])
        if self.avatar:
            return self.avatar[0].render()
        else:
            return f"""<img src={url_for('static', filename='img/default-avatar.jpg')} {attrs}>"""

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, value):
        self.hashed_password = generate_password_hash(value)
    
    @property
    def full_name(self):
        return f'{self.surname} {self.name}'

    @property
    def login(self):
        return self.user_login if self.user_login else self.id

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<User> id: {self.id} name: {self.name}'