import os
from typing import Union
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")

class Dish(BaseModel):
    name: str
    description: Union[str, None] = None
    size: int
    sauce: bool
    base_price: int


app = FastAPI()

name = 'Иван'
UPLOAD_DIRECTORY = "images"
app.mount("/static", StaticFiles(directory=UPLOAD_DIRECTORY), name="static")

@app.post("/order/")
async def get_pizza(dish: Dish):
    return {
        "ordered": dish,
        "price": dish.base_price * 1.5
    }

@app.get("/test_page")
async def get_test_page(request: Request):
    return templates.TemplateResponse("new_page.html", {"request": request, "user": name})


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())

    return {"info": f"File '{file.filename}' saved at '{file_location}'"}

@app.get("/image_page")
async def get_test_page(request: Request):
    return templates.TemplateResponse("image.html",
                                      {"request": request,
                                       "image_url": f"/static/{os.listdir(UPLOAD_DIRECTORY)[-1]}"})