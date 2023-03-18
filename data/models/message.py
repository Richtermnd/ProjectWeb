import datetime
import sqlalchemy
from sqlalchemy import orm
from ..db_session import SqlAlchemyBase


class Message(SqlAlchemyBase):
    __tablename__ = 'messages'

    # model fields
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True,
                           unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('chats.id'))
    date_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    is_text = sqlalchemy.Column(sqlalchemy.Boolean)
    text = sqlalchemy.Column(sqlalchemy.Boolean)
    is_file = sqlalchemy.Column(sqlalchemy.Boolean)
    file_id = sqlalchemy.Column(sqlalchemy.ForeignKey('files.id'))

    # many to one
    user = orm.relationship('User')
    chat = orm.relationship('Chat')
    file = orm.relationship('File')

    def __repr__(self):
        return f'<Message> id: {self.id} sender: {self.user} chat: {self.chat}'
