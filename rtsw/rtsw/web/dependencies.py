from functools import cache
from typing import Annotated

import psycopg as pg
from fastapi import Depends

from rtsw.persist import connect_db_from_env, query
from rtsw.shared import RtswDataPoint


def _get_db():
    with connect_db_from_env() as conn:
        yield conn


Database = Annotated[pg.Connection, Depends(_get_db)]


class _db_func:
    def __init__(self, f, *args, **kwargs) -> None:
        self._f = f
        self._args = args
        self._kwargs = kwargs

    def __call__(self, db: Database) -> None:
        return self._f(db, *self._args, **self._kwargs)


def get_points(db: Database, limit: int = 1000):
    return query.get_rtsw_points(db, limit)


RtswPoints = Annotated[list[RtswDataPoint], Depends(get_points)]
