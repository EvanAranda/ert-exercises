from datetime import datetime, timedelta
from time import sleep
from typing import Generator, Optional

import httpx
from pydantic import BaseModel

_client = httpx.Client(base_url="https://services.swpc.noaa.gov")


class HourlyRtswPoint(BaseModel):
    time_tag: datetime
    propagated_time_tag: datetime
    speed: float
    density: float
    temperature: float
    bx: Optional[float]
    by: Optional[float]
    bz: Optional[float]
    bt: Optional[float]
    vx: Optional[float]
    vy: Optional[float]
    vz: Optional[float]


def fetch_hourly_rtsw_json() -> list[HourlyRtswPoint]:
    """
    Fetches the latest 24 hours of hourly RSTW data from NOAA and returns
    the data points in descending order by time tag.
    """
    res = _client.get("/products/geospace/propagated-solar-wind-1-hour.json")
    data: list[list] = res.json()
    dicts = [dict(zip(data[0], row)) for row in data[1:]]
    points = list(map(HourlyRtswPoint.model_validate, dicts))
    points.sort(key=lambda p: p.time_tag, reverse=True)
    return points


def ticker(f: timedelta) -> Generator[int, None, None]:
    """
    Emits a tick when the current time is a multiple of `f`
    """

    # origin time
    o = datetime.now()
    o = datetime(o.year, o.month, o.day, 0, 0, 0)

    i = 0

    while True:
        t = datetime.now()

        dt = t - o

        # seconds after time was last a multiple of `f`
        dt_next = dt.total_seconds() % f.total_seconds()
        sleep_time = f.total_seconds() - dt_next
        sleep_time = max(sleep_time, 0)
        sleep(sleep_time)
        yield i
        i += 1


def parse_time(time_str: str) -> timedelta:
    """
    Parses a time string of the form [[HH:]MM:]SS into a timedelta
    """
    parts = time_str.split(":")
    h, m, s = 0, 0, 0
    if len(parts) > 0:
        s = int(parts[-1])
    if len(parts) > 1:
        m = int(parts[-2])
    if len(parts) > 2:
        h = int(parts[-3])
    return timedelta(hours=h, minutes=m, seconds=s)
