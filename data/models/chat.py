import sqlalchemy
from sqlalchemy import orm
from ..db_session import SqlAlchemyBase
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

    # one to many
    messages = orm.relationship('Message',
                                back_populates='chat')

    # many to many
    users = orm.relationship('User',
                             secondary=UserToChat,
                             back_populates='chats')

    def __repr__(self):
        return f'<Chat> id: {self.id} name: {self.name}'
