import os

import psycopg as pg
from psycopg.rows import dict_row

from rtsw.shared import HourlyRtswPoint, fetch_hourly_rtsw_json


def connect_db(db_url: str) -> pg.Connection:
    return pg.connect(db_url)


def connect_db_from_env() -> pg.Connection:
    return connect_db(os.environ["DATABASE_URL"])
