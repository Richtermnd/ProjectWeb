import datetime

from .base_form import BaseForm
from wtforms.fields import StringField, PasswordField, EmailField, DateField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from .custom_validators import UniqueEmail

from data.models import User
from data import db_session


class LoginForm(BaseForm):
    _ignore_fields = BaseForm._ignore_fields + ['confirm_password']
    name = StringField('Name',
                       validators=[DataRequired('Required Field')],
                       render_kw={'placeholder': 'Name'})

    surname = StringField('Surname',
                          validators=[DataRequired('Required Field')],
                          render_kw={'placeholder': 'Surname'})

    email = EmailField('Email',
                       validators=[DataRequired('Required Field'),
                                   UniqueEmail()],
                       render_kw={'placeholder': 'Email'})

    birthdate = DateField('Birthdate',
                          validators=[DataRequired('Required Field')],
                          render_kw={'max': datetime.date.today().strftime('%Y-%m-%d')})

    password = PasswordField('Password',
                             validators=[DataRequired('Required Field')],
                             render_kw={'placeholder': 'Password'})

    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired('Required Field'),
                                                 EqualTo('password', message='Passwords should be the same')],
                                     render_kw={'placeholder': 'Password'})

    submit = SubmitField('Login')

    def login_user(self):
        # creating and adding user to db
        with db_session.create_session() as session:
            session.add(User(**self.data))
            session.commit()
