import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from storage.onedrive import OneDrive

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


try:
    onedrive = OneDrive.init_from_env()
except KeyError:
    onedrive = OneDrive.init_from_json(
        os.path.normpath(os.path.join(os.path.dirname(__file__), "../auth.json"))
    )


@app.get("/")
async def list_or_get_file(request: Request):
    file_info_list = onedrive.ls_folder("")
    file_info_list = [i._asdict() for i in file_info_list]
    return templates.TemplateResponse(
        "index.html",
        context={"request": request, "file_info_list": file_info_list},
    )


@app.get("/{file_path:path}")
async def downloader(file_path: str):
    download_link = onedrive.get_download_link(file_path)
    if download_link:
        return RedirectResponse(download_link, status_code=307)
    else:
        return HTTPException(404, f"{file_path} is not exist.")
