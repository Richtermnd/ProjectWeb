import datetime

from tools import create_file

from .base_form import BaseForm
from wtforms.fields import StringField, EmailField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from .custom_validators import UniqueValue

from data.models import User
from data import db_session


class UserForm(BaseForm):
    _ignore_fields = BaseForm._ignore_fields
    avatar = FileField('Avatar')
    name = StringField('Name',
                       validators=[DataRequired('Required Field')],
                       render_kw={'placeholder': 'Name'})

    surname = StringField('Surname',
                          validators=[DataRequired('Required Field')],
                          render_kw={'placeholder': 'Surname'})

    user_login = StringField('Surname',
                                 validators=[UniqueValue(User.user_login)],
                                 render_kw={'placeholder': 'Personal login'})

    email = EmailField('Email',
                       validators=[DataRequired('Required Field')],
                       render_kw={'placeholder': 'Email'})

    birthdate = DateField('Birthdate',    
                          render_kw={'max': datetime.date.today().strftime('%Y-%m-%d')})

    about = StringField('About',
                        render_kw={'placeholder': 'About'})
    
    contact_email = EmailField('Contact Email',
                       render_kw={'placeholder': 'Contact Email'})
    
    submit = SubmitField('Confirm')

    def confirm_changes(self, user: User):
        with db_session.create_session() as session:
            # avatar is hard
            user = session.get(User, user.id)  # idk, but without this doesn't work commit
            user.name = self.name.data
            user.surname = self.surname.data
            user.user_login = self.user_login.data
            user.email = self.email.data
            user.birthdate = self.birthdate.data
            user.about = self.about.data
            user.contact_email = self.contact_email.data
            session.commit()
