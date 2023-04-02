from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    _ignore_fields = ['csrf_token', 'submit']

    @property
    def data(self):
        data = super().data
        for field in self._ignore_fields:
            data.pop(field)
        return data
