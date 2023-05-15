import argparse
from sqlalchemy_utils.functions import drop_database

def drop_db():
    conn_str = f'sqlite:///db/db.db?check_same_thread=False'
    drop_database(conn_str)


FUNC_MAP = {
    'drop_db': drop_db
}

parser = argparse.ArgumentParser()
parser.add_argument('func', type=str)


args = parser.parse_args()
FUNC_MAP[args.func]()