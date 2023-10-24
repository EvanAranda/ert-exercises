from importlib.resources import files

import plotly.express as px
from fastapi import APIRouter, FastAPI, Request
from fastapi.templating import Jinja2Templates

from rtsw.shared import rtsw_to_df

from .dependencies import RtswPoints

app = FastAPI()
api = APIRouter()
app.mount("/api", api)

templates = Jinja2Templates(directory=str(files("rtsw.web").joinpath("templates")))


def _tohtml(fig):
    return fig.to_html(full_html=False, include_plotlyjs=False)


@app.get("/")
def get_dashboard(request: Request, points: RtswPoints):
    df = rtsw_to_df(points)

    chart_infos = [
        ("B", ["bx", "by", "bz", "bt"]),
        ("V", ["vx", "vy", "vz"]),
        ("Speed", "speed"),
        ("Density", "density"),
        ("Temperature", "temperature"),
    ]

    charts = [px.line(df, x=df.index, y=y, title=title) for title, y in chart_infos]

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "points": points,
            "charts": list(map(_tohtml, charts)),
        },
    )


@api.get("/rtsw")
def get_rtsw(points: RtswPoints):
    return points
