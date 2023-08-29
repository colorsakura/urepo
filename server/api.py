import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from storage.onedrive import OneDrive

app = FastAPI()

try:
    onedrive = OneDrive.init_from_env()
except KeyError:
    onedrive = OneDrive.init_from_json(
        os.path.normpath(os.path.join(os.path.dirname(__file__), "../auth.json"))
    )


@app.get("/{file_path:path}")
async def downloader(file_path: str):
    download_link = onedrive.get_download_link(file_path)
    if download_link:
        return RedirectResponse(download_link, status_code=307)
    else:
        return HTTPException(404, f"{file_path} is not exist.")
