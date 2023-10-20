import psycopg as pg
from psycopg.rows import dict_row

from rtsw.shared import HourlyRtswPoint, fetch_hourly_rtsw_json


def sync_rtsw(conn: pg.Connection, points: list[HourlyRtswPoint]):
    with conn.cursor() as cur:
        stmt = """
        insert into rtsw (time_tag, propagated_time_tag, speed, density, temperature, bx, by, bz, bt, vx, vy, vz) 
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        on conflict (time_tag) do nothing
        """
        for p in points:
            cur.execute(
                stmt,
                (
                    p.time_tag,
                    p.propagated_time_tag,
                    p.speed,
                    p.density,
                    p.temperature,
                    p.bx,
                    p.by,
                    p.bz,
                    p.bt,
                    p.vx,
                    p.vy,
                    p.vz,
                ),
            )


def sync_rtsw_hourly(conn: pg.Connection):
    points = fetch_hourly_rtsw_json()
    sync_rtsw(conn, points)


def get_rtsw_points(conn: pg.Connection):
    with conn.cursor(row_factory=dict_row) as cur:
        results = cur.execute("select * from rtsw order by time_tag asc").fetchall()
        return list(map(HourlyRtswPoint.model_validate, results))
