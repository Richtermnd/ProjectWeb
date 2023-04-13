from flask import render_template, url_for
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from ..db_session import SqlAlchemyBase, create_session
from .association_tables import Friends, Likes, UserToChat, Avatars

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
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    birthdate = sqlalchemy.Column(sqlalchemy.Date)

    # optional info
    about = sqlalchemy.Column(sqlalchemy.String)
    contact_email = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    avatar = orm.relationship('File', secondary=Avatars)

    # one to many
    messages = orm.relationship('Message', 
                                back_populates='user')
    files = orm.relationship('File', 
                             back_populates='user')
    posts = orm.relationship('Post', 
                             back_populates='user')

    # many to many
    chats = orm.relationship('Chat',
                             secondary=UserToChat,
                             back_populates='users')
    likes = orm.relationship('Post',
                             secondary=Likes,
                             back_populates='likes')
    friends = orm.relationship('Friends',
                               back_populates='user1',
                               primaryjoin=id == Friends.user1_id,
                               join_depth=5)
    
    def form_data(self):
        data = {
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'birthdate': self.birthdate,
            'about': self.about,
            'contact_email': self.contact_email
        }
        return data
    
    def friends_choices(self):
        return [(user.user2_id, user.user2.full_name) for user in self.friends]
    
    def not_in_chat_friends(self, chat):
        return list(filter(lambda x: x not in chat.users, self.friends))
    
    def render_chat_list(self):
        return render_template('chat_list.jinja', user=self)
    
    def render_card(self, is_friend=False):
        return render_template('user_card.jinja', user=self, is_friend=is_friend)
    
    def get_avatar(self, **kwargs):
        attrs = ' '.join([f'{key}="{value}"' for key, value in kwargs.items()])
        if self.avatar:
            return self.avatar[0].render(**kwargs)
        else:
            return f"""<img src={url_for('static', filename='img/default-avatar.jpg')} {attrs}>"""
    
    def recomendations(self):
        all_posts = []
        for friend in self.friends:
            all_posts.extend(friend.user2.posts)
        return sorted(all_posts, key=lambda x: x.date_time)
  
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
    def short_name(self):
        return f'{self.surname[0]}. {self.name}'

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<User> id: {self.id} name: {self.name}'
    