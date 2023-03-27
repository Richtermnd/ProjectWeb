from .base_form import BaseForm
from wtforms.fields import SubmitField, TextAreaField, MultipleFileField

from data.models import Post, FileContainer, CommentsChat
from data import db_session
from flask_login import current_user

from tools import create_file


class PostForm(BaseForm):
    _ignore_fields = BaseForm._ignore_fields
    text = TextAreaField('Text of the post', render_kw={'placeholder': 'Enter text of the post'})
    files = MultipleFileField('Files')
    submit = SubmitField('Post')

    def create_post(self):
        with db_session.create_session() as session:
            # Loading and adding files
            if self.files.data:
                container = FileContainer()
                for file_data in self.files.data:
                    file = create_file(file_data)
                    container.files.append(file)
                print(len(container.files))
            
            post = Post()

            # user
            post.user_id = current_user.id

            # text
            post.is_text = bool(self.text.data)
            post.text = self.text.data

            # files
            post.is_file = bool(self.files.data)
            post.file_container = container

            # chat
            chat = CommentsChat(post=[post])
            post.chat = chat

            session.add(post)
            session.commit()
        return post


