from wtforms.validators import ValidationError

from data import db_session
from data import models


def UniqueValue(attr, message='User with this email already exist'):
    def _validator(form, field):
        email = field.data.strip()
        session = db_session.create_session()
        if session.query(models.User).filter(attr == email).all():
            raise ValidationError(message)
    return _validator


def NotEmpty(message='Empty message'):
    def _validator(form, field):
        is_text = bool(form.text.data)
        is_file = any(filter(lambda x: x.filename != '', form.files.data))
        if is_text or is_file:
            return is_text or is_file
        else:
            print(message)
            raise ValidationError(message)
    return _validator
