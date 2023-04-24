from flask import render_template, url_for
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from ..db_session import SqlAlchemyBase, create_session
from .association_tables import UserToChat


class Chat(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'chats'
    __mapper_args__ = {
        "polymorphic_identity": "chats",
        "polymorphic_on": 'type'
    }

    # model fields
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True,
                           unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    is_public = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    type = sqlalchemy.Column(sqlalchemy.String)
    avatar_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                  sqlalchemy.ForeignKey('files.id'))
    creator_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    avatar = orm.relationship('File', foreign_keys=[avatar_id])

    creator = orm.relationship('User', 
                               foreign_keys=[creator_id])

    # one to many
    messages = orm.relationship('Message',
                                back_populates='chat')

    # many to many
    users = orm.relationship('User',
                             secondary=UserToChat,
                             back_populates='chats')
    
    def form_data(self):
        data = {
            'name': self.name,
            'is_public': self.is_public
        }
        return data
    
    def add_users(self, *users):
        self.users.extend(users)
    
    def render(self, form):
        return render_template('chat.jinja', chat=self, form=form)
    
    def avatar_render(self, **kwargs):
        if self.avatar:
            return self.avatar.render(**kwargs)
        else:
            attrs = ' '.join([f'{key}="{value}"' for key, value in kwargs.items()])
            return f"""<img src={url_for('static', filename='img/default-avatar.jpg')} {attrs}>"""
    
    def render_last_message(self):
        if self.last_message:
            return self.last_message.preview_render()
        else:
            return 'Нет сообщений.'
    
    @property
    def last_message(self):
        if self.messages:
            return self.messages[-1]
        else:
            return None

    def preview_render(self):
        return render_template('chat_preview.jinja', chat=self)

    def __repr__(self):
        return f'<Chat> id: {self.id} name: {self.name}'
