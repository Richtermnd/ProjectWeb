from flask_login import current_user

from tools import create_file

from .base_form import BaseForm
from wtforms.fields import StringField, SubmitField, BooleanField, SelectMultipleField, FileField

from data.models import Chat, User, UserToChat
from data import db_session


class ChatForm(BaseForm):
    _ignore_fields = BaseForm._ignore_fields + ['users']

    avatar = FileField('Avatar')
    
    name = StringField('Chat name', render_kw={'placeholder': 'Enter chat name', 
                                               'autocomplete': "off"})
    is_public = BooleanField('Is public')

    users = SelectMultipleField(coerce=int, validate_choice=False)

    submit = SubmitField('Submit')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.users.choices = current_user.friends_choices()

    def create_chat(self):
        with db_session.create_session() as session:
            chat = Chat(**self.data)
            chat.creator_id = current_user.id
            chat.users.append(session.get(User, current_user.id))
            for user_id in self.users.data:
                chat.users.append(session.get(User, user_id))
            session.add(chat)
            session.commit()
            chat.avatar = create_file(self.avatar.data)
            session.merge(chat)
        return chat
    
    def update(self, chat):
        with db_session.create_session() as session:
            chat = session.get(Chat, chat.id)
            chat.name = self.name.data
            chat.is_public = self.is_public.data
            for user_id in self.users.data:
                chat.users.append(session.get(User, user_id))
            session.commit()
