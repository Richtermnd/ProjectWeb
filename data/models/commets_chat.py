import sqlalchemy
from sqlalchemy import orm

from .chat import Chat


class CommentsChat(Chat):
    __tablename__ = 'comments_chats'
    __mapper_args__ = {
        "polymorphic_identity": "comments_chats"
    }

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           sqlalchemy.ForeignKey('chats.id'),
                           primary_key=True,
                           autoincrement=True,
                           unique=True)
    post = orm.relationship('Post')

    def __repr__(self):
        return f'<CommentsChat> id {self.id} post: {self.post}'
