import pandas as pd
from datetime import datetime
from typing import Optional, Sequence

import httpx
from pydantic import BaseModel

_client = httpx.Client(base_url="https://services.swpc.noaa.gov")


class RtswDataPoint(BaseModel):
    time_tag: datetime
    propagated_time_tag: datetime
    speed: Optional[float]
    density: Optional[float]
    temperature: Optional[float]
    bx: Optional[float]
    by: Optional[float]
    bz: Optional[float]
    bt: Optional[float]
    vx: Optional[float]
    vy: Optional[float]
    vz: Optional[float]


def fetch_hourly_rtsw_json() -> list[RtswDataPoint]:
    """
    Fetches the latest 24 hours of hourly RSTW data from NOAA and returns
    the data points in descending order by time tag.
    """
    res = _client.get("/products/geospace/propagated-solar-wind-1-hour.json")
    return to_datapoint_model(res.json())


def fetch_full_rtsw_json() -> list[RtswDataPoint]:
    res = _client.get("/products/geospace/propagated-solar-wind.json")
    return to_datapoint_model(res.json())


def to_datapoint_model(data: Sequence[dict]) -> list[RtswDataPoint]:
    dicts = [dict(zip(data[0], row)) for row in data[1:]]
    points = list(map(RtswDataPoint.model_validate, dicts))
    points.sort(key=lambda p: p.time_tag)
    return points


def rtsw_to_df(points: Sequence[RtswDataPoint]) -> pd.DataFrame:
    df = pd.DataFrame.from_records(data=map(RtswDataPoint.model_dump, points))
    df.set_index("time_tag", inplace=True)
    return df
