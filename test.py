from data.models import *
from data.db_session import create_session, global_init


global_init('db/test.db')
session = create_session()

