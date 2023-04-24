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

    email = EmailField('Email',
                       validators=[DataRequired('Required Field')],
                       render_kw={'placeholder': 'Email'})

    birthdate = DateField('Birthdate',    
                          render_kw={'max': datetime.date.today().strftime('%Y-%m-%d')})

    about = StringField('About',
                        render_kw={'placeholder': 'About'})
    address = StringField('address',
                        render_kw={'placeholder': 'Address'})
    
    contact_email = EmailField('Contact Email',
                       render_kw={'placeholder': 'Contact Email'})
    
    submit = SubmitField('Confirm')

    def confirm_changes(self, user: User):
        if self.avatar.data:
            file = create_file(self.avatar.data)
        with db_session.create_session() as session:
            # avatar is hard
            print(self.avatar.data)
            user = session.get(User, user.id)
            user.name = self.name.data
            user.surname = self.surname.data
            user.email = self.email.data
            user.birthdate = self.birthdate.data
            user.about = self.about.data
            user.address = self.address.data
            user.contact_email = self.contact_email.data
            if self.avatar.data:
                user.avatar = [file]
            session.commit()
