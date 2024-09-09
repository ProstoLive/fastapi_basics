from typing import Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class Aboba:
    def __init__(self, name: str):
        self.name = name
        self.data = "Aboba is awesome!"

@app.get("/")
async def root(person: Annotated[dict, Depends(Aboba)]):
    return person