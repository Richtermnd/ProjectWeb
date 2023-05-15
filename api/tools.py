import re
from data import db_session
from flask_restful import abort


def not_found_factory(model: db_session.SqlAlchemyBase):
    def func(_id):
        with db_session.create_session() as session:
            obj = session.get(model, _id)
            if not obj:
                abort(404, message=f"Object with {_id} not found")
    return func


def correct_date_format(date: str):
    res = re.search(r'\d{2,4}-\d{1,2}-\d{1,2}', date)
    return bool(res)