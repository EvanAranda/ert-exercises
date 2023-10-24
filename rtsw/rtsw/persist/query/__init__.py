import psycopg as pg
from psycopg import sql, rows

from rtsw.shared import RtswDataPoint, fetch_hourly_rtsw_json


def sync_rtsw(conn: pg.Connection, points: list[RtswDataPoint]):
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


def get_rtsw_points(conn: pg.Connection, limit: int):
    stmt = sql.SQL(
        """
        select * from rtsw
        order by time_tag asc
        limit {limit}
        """
    )

    stmt = stmt.format(limit=sql.Literal(limit))

    with conn.cursor(row_factory=rows.dict_row) as cur:
        results = cur.execute(stmt).fetchall()
        return list(map(RtswDataPoint.model_validate, results))
