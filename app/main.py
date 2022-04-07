from logging import exception
from sqlite3 import Cursor
from typing import Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, BaseSettings
from random import randrange


from fastapi.middleware.cors import CORSMiddleware

from typing import Optional, List

import time
from sqlalchemy.orm import Session


from . import models
from . import schemas, utils
from .database import engine, get_db
from . routers import admin, auth, slots, subadmin, bay, clients, products, clients_products
from .config import settings


import schedule
import time


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


data = [{"title": "Mounika", "content": "gvp", "id": 1},
        {"title": "Jogendra", "content": "gvpce", "id": 2}]


def find(id):
    for p in data:
        if p["id"] == id:
            return p


def find_index(id):
    for i, p in enumerate(data):
        if p['id'] == id:
            return i


app.include_router(admin.router)
app.include_router(subadmin.router)
app.include_router(clients.router)
app.include_router(products.router)
app.include_router(bay.router)
app.include_router(slots.router)
app.include_router(clients_products.router)
app.include_router(auth.router)

# app.include_router(vote.router)


@app.get("/")
async def root():
    return {"Message": "Welcome to East India Petroleum LTD slot booking system"}


def geeks():
    print("Shaurya says Geeksforgeeks")


# Task scheduling
# After every 10mins geeks() is called.
schedule.every(5).seconds.do(geeks)


# while True:

# 	# Checks whether a scheduled task
# 	# is pending to run or not
# 	schedule.run_pending()
# 	time.sleep(1)
