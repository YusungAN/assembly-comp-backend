from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from api.views import router as api_router

import models


from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from datetime import date, datetime
# from fastapi_scheduler import SchedulerAdmin
from fastapi.middleware.cors import CORSMiddleware




from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn

templates = Jinja2Templates(directory="static")


app = FastAPI()

app.include_router(api_router, prefix="/api", tags=["api"])

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})






@app.on_event("startup")
async def startup():
    # Mount the background management system

    # remove all images at /result/images
    import os
    # providing the path of the folder
    # r = raw string literal
    folder_path = os.path.dirname(os.path.abspath(__file__))  + '/result/images'
    # using listdir() method to list the files of the folder
    test = os.listdir(folder_path)

    # taking a loop to remove all the images
    # using ".png" extension to remove only png images
    # using os.remove() method to remove the files
    for images in test:
        if images.endswith(".jpg"):
            os.remove(os.path.join(folder_path, images))


    app.mount("/web", StaticFiles(directory="static"), name="static")

    # Start the scheduled task scheduler
    # scheduler.start()

    # init_schedule()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

