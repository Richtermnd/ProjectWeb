from flask import render_template, url_for
import sqlalchemy
from sqlalchemy import orm
from ..db_session import SqlAlchemyBase, create_session
from .association_tables import UserToChat


class Chat(SqlAlchemyBase):
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
    avatar = orm.relationship('File', lazy='selectin')

    # one to many
    messages = orm.relationship('Message',
                                back_populates='chat', 
                                lazy='selectin')

    # many to many
    users = orm.relationship('User',
                             secondary=UserToChat,
                             back_populates='chats', 
                             lazy='dynamic')
    
    def render(self, form):
        return render_template('chat.jinja', chat=self, form=form)
    
    def avatar_render(self, **kwargs):
        if self.avatar:
            return self.avatar.render(**kwargs)
        else:
            attrs = ' '.join([f'{key}="{value}"' for key, value in kwargs.items()])
            return f"""<img src={url_for('static', filename='img/default-avatar.jpg')} {attrs}>"""
    
    def render_last_message(self):
        if self.messages:
            return self.messages[-1].preview_render()
        else:
            return 'Нет сообщений.'

    def preview_render(self):
        return render_template('chat_preview.jinja', chat=self)

    def __repr__(self):
        return f'<Chat> id: {self.id} name: {self.name}'
    
    def __getattribute__(self, __name: str):
        with create_session():
            return super().__getattribute__(__name)
        
