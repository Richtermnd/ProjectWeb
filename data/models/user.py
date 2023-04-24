from flask import render_template, url_for
import requests
import sqlalchemy
from sqlalchemy import orm
from flask_login import AnonymousUserMixin, UserMixin, current_user
from sqlalchemy_serializer import SerializerMixin

from config import YANDEX_API_KEY

from ..db_session import SqlAlchemyBase, create_session
from .association_tables import Friends, Likes, UserToChat, Avatars

from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
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
                               lazy='joined')
    
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
        with create_session() as session:
            s = session.get(User, self.id)
            return [(user.user2_id, user.user2.full_name) for user in s.friends]
    
    def not_in_chat_friends(self, chat):
        return list(filter(lambda x: x not in chat.users, self.friends))
    
    def render_chat_list(self):
        return render_template('chat_list.jinja', user=self)
    
    def render_card(self, is_friend=False):
        return render_template('user_card.jinja', user=self, is_friend=is_friend)
    
    def get_map(self, **kwargs):
        if not self.address:
            return ''
        
        attrs = ' '.join([f'{key}="{value}"' for key, value in kwargs.items()])
        def get_pos(user_):
            url = 'http://geocode-maps.yandex.ru/1.x/'
            params = {
                'apikey': YANDEX_API_KEY,
                'geocode': user_.address,
                'format': 'json'
            }
            response_ = requests.get(url, params=params).json()
            return response_['response']["GeoObjectCollection"]['featureMember'][0]['GeoObject']['Point']['pos'].split()
        
        url = 'https://static-maps.yandex.ru/1.x/?'
        params = {
            'l': 'map',
            'pt': '{},{},pm2bll'.format(*get_pos(self))
        }
        if isinstance(current_user, AnonymousUserMixin) or self.id == current_user.id:
            params['spn'] = '0.1,0.1'
        else:
            if current_user.address:
                params['pt'] += '~{},{},pm2dol'.format(*get_pos(current_user))
            else:
                params['spn'] = '0.1,0.1'
        params = '&'.join([f'{key}={value}' for key, value in params.items()])
        return f'<img src="{url + params}" {attrs}>'
    
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
        return sorted(all_posts, key=lambda x: x.date_time, reverse=True)
  
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
    