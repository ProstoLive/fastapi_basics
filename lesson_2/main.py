from fastapi import FastAPI
from typing import Annotated
from fastapi import Query
from enum import Enum

class Transport(str, Enum):
    bus = "bus"
    bike = "bike"
    plane = "plane"
    my_own_feet = "my_own_feet"

app = FastAPI()

@app.post("/email")
async def email_validation(email: Annotated[str, Query(pattern="^[a-z0-9]+@[a-z0-9]+\.[a-z0-9]+$")]):
    return {"email": email}

@app.post("/phone_number")
async def phone_validation(phone_number: Annotated[str, Query(pattern="^\+7\d{10}$")]):
    return {"phone_number": phone_number}

@app.post("/a_lot_of_parameters")
async def give_me_a_list(q: Annotated[list[int], Query(min_length=2)]):
    return {"q": q}

@app.post("/age")
async def age(age: Annotated[int, Query(gt=18, le=100)]):
    return {"age": age}

@app.post("/how_to_get_home/{transport}")
async def how_to_get_home(transport: Transport):
    return {"how_to_get_home": transport}