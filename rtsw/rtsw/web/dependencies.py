from functools import cache
from typing import Annotated

import psycopg as pg
from fastapi import Depends

from rtsw.persist import connect_db_from_env
from rtsw.persist.query import get_rtsw_points
from rtsw.shared import HourlyRtswPoint


@cache
def _get_db() -> pg.Connection:
    return connect_db_from_env()


Database = Annotated[pg.Connection, Depends(_get_db)]


class _db_func:
    def __init__(self, f, *args, **kwargs) -> None:
        self._f = f
        self._args = args
        self._kwargs = kwargs

    def __call__(self, db: Database) -> None:
        return self._f(db, *self._args, **self._kwargs)


RtswPoints = Annotated[list[HourlyRtswPoint], Depends(_db_func(get_rtsw_points))]
