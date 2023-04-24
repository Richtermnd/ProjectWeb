import datetime
from flask import render_template
import sqlalchemy
from sqlalchemy import orm
from ..db_session import SqlAlchemyBase, create_session
from sqlalchemy_serializer import SerializerMixin


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'messages'

    # model fields
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True,
                           unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('chats.id'))
    date_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    is_text = sqlalchemy.Column(sqlalchemy.Boolean)
    text = sqlalchemy.Column(sqlalchemy.String)

    is_file = sqlalchemy.Column(sqlalchemy.Boolean)
    file_container_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('file_containers.id'))

    # many to one
    user = orm.relationship('User')
    chat = orm.relationship('Chat')
    file_container = orm.relationship('FileContainer')

    def preview_render(self):
        # with create_session():
        if self.is_text:
            # text = f'{self.user.name}: {self.text}'  fix this
            text = f'{self.text}'
            if len(text) > 30:
                return f"""<span class="chat-preview-last-message">{text[:30]}...</span>"""
            else:
                return f"""<span class="chat-preview-last-message">{text}</span>"""
        elif self.is_file:
            return f"""<span class="chat-preview-last-message">File</span>"""
        else:
            return ''
    
    def render(self):
        with create_session():
            return render_template('message.jinja', message=self)

    @property
    def files(self):
        return self.file_container.files

    def __repr__(self):
        return f'<Message> id: {self.id} sender: {self.user} chat: {self.chat}'
    
    def __lt__(self, other):
        if other:
            return self.date_time < other.date_time
        else:
            return True

    def __eq__(self, other):
        if other:
            return self.date_time == other.date_time
        else:
            return False