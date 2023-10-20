from importlib.resources import files
from pathlib import Path
from fastapi import APIRouter, FastAPI, Request
from fastapi.templating import Jinja2Templates

from .dependencies import RtswPoints

app = FastAPI()
api = APIRouter()
app.mount("/api", api)

templates = Jinja2Templates(directory=str(files("rtsw.web").joinpath("templates")))


@app.get("/")
def get_dashboard(request: Request, points: RtswPoints):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "points": points},
    )


@api.get("/rtsw")
def get_rtsw(points: RtswPoints):
    return points
