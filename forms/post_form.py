import datetime
from .base_form import BaseForm
from wtforms.fields import SubmitField, TextAreaField, MultipleFileField

from data.models import Post, FileContainer, CommentsChat
from data import db_session
from flask_login import current_user

from tools import create_file


class PostForm(BaseForm):
    _ignore_fields = BaseForm._ignore_fields + ['files']
    text = TextAreaField('Text of the post', render_kw={'placeholder': 'Enter text of the post'})
    files = MultipleFileField('Files')
    submit = SubmitField('Post')

    def create_post(self):
        with db_session.create_session() as session:
            data = self.data
            data['is_text'] = bool(self.text.data)
            true_files = list(filter(lambda x: x.filename != '', self.files.data))
            data['is_file'] = any(true_files)
            post = Post(**data)
            if data['is_file']:
                container = FileContainer()
                for file_data in true_files:
                    create_file(file_data, container)
                post.file_container = container
            post.user = current_user
            comments_chat = CommentsChat()
            post.chat = comments_chat
            session.add(post)
            session.commit()
            post.name= f'Comments to post {post.id}'
            session.commit()
            return post
