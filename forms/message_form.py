import datetime

from .base_form import BaseForm
from wtforms.fields import StringField, MultipleFileField, SubmitField
from .custom_validators import NotEmpty
from markupsafe import Markup

from data.models import FileContainer, Message
from data import db_session
from tools import create_file


class MessageForm(BaseForm):
    _ignore_fields = BaseForm._ignore_fields + ['files']
    
    text = StringField(render_kw={'placeholder': 'Enter message', 
                                  'autocomplete': "off"})
    files = MultipleFileField()

    submit = SubmitField(Markup(''),
                         validators=[NotEmpty()])

    def create_message(self, user, chat):
        data = self.data
        data['date_time'] = datetime.datetime.now()
        data['is_text'] = bool(self.text.data)
        true_files = list(filter(lambda x: x.filename != '', self.files.data))
        data['is_file'] = any(true_files)
        message = Message(**data)
        if data['is_file']:
            container = FileContainer()
            for file_data in true_files:
                create_file(file_data, container)
            if len(container.files) > 0:
                message.file_container = container
        message.chat_id = chat.id
        message.user = user
        with db_session.create_session() as session:
            session.add(message)
            session.commit()
        return message
