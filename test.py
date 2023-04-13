from data.models import *
from data.db_session import create_session, global_init


global_init('db/db.db')
session = create_session()

