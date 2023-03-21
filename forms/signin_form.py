import datetime

from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired
from .form_exeptions import *

from data.models import User
from data import db_session


class SignInForm(FlaskForm):
    email = EmailField(
        validators=[DataRequired('Required Field')], 
        render_kw={'placeholder': 'Email'}
    )
    password = PasswordField(
        validators=[DataRequired('Required Field')],
        render_kw={'placeholder': 'Password'}
    )
    remember = BooleanField(
        'Remember me'
    )
    submit = SubmitField('Sign in')

    def get_user(self):
        with db_session.create_session() as session:
            user = session.query(User).filter(User.email == self.email.data).first()
            if user is None:
                raise UserNotExistException
            if not user.check_password(self.password.data):
                raise WrongPasswordException
            return {'user': user, 'remember': self.remember.data}
            
