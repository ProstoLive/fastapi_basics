import json
import os
from uuid import UUID

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel, Field
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

app = FastAPI()
templates = Jinja2Templates(directory="templates")
IMAGES_DIRECTORY = "images"
POSTS_DIRECTORY = "posts"

class UploadPost(BaseModel):
    id: int
    name: str
    description: str = Field(max_length=200)

@app.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})

@app.post("/upload")
async def upload_post(post: UploadPost = Depends(), file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="File type not supported")

    image_location = f"{IMAGES_DIRECTORY}/{file.filename}"
    with open(image_location, "wb+") as file_object:
        file_object.write(await file.read())

    post_location = f"{POSTS_DIRECTORY}/{post.name}"
    data_dump = jsonable_encoder(post)
    data_dump["image_url"] = image_location
    with open(post_location, "w+") as post_object:
        json.dump(data_dump, post_object)

@app.get("/galery")
async def galery(request: Request):
    posts = []
    for filename in os.listdir(POSTS_DIRECTORY):
        file_path = os.path.join(POSTS_DIRECTORY, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            posts.append(json.load(file))
    return templates.TemplateResponse("galery.html", {"request": request, "posts": posts})

@app.get("/post/{id}")
async def get_post(request: Request, id: int):
    pass