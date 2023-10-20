import os
import uvicorn

is_dev = os.getenv("ENV", "dev") == "dev"
uvicorn.run("rtsw.web:app", reload=is_dev)
