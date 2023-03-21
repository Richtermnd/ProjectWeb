from wtforms.validators import ValidationError

from data import db_session
from data import models


def UniqueEmail(message='User with this email already exist'):
    def _validator(form, field):
        email = field.data.strip()
        session = db_session.create_session()
        if session.query(models.User).filter(models.User.email == email).all():
            raise ValidationError(message)

    return _validator
