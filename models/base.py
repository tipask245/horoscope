from models.sql import *


class Base:
    db, cursor = connect_db(DB_PATH)
