from datetime import datetime
from typing import Optional

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
