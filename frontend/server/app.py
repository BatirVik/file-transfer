from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

STATIC_PATH = Path(__file__).parent / "static"

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_PATH))


@app.get("/{full_path:path}")
async def index():
    return FileResponse(STATIC_PATH / "index.html")
