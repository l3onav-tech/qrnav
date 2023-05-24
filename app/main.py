from fastapi import FastAPI, Request, HTTPException, Depends, status
from app.settings import r as redis
from functools import lru_cache
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.users import models
from app.settings.database import engine
import os
from app.users import urls as users_urls
#database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://api.localhost",
]

app.include_router(users_urls.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main(request: Request):
    clientIp = request.client.host
    urls = [{"path": route.path, "name": route.name} for route in request.app.routes]
    return {
        "message": "Hello World",
        "env": os.getenv("ENVIROMENT", "development"),
        "clientIp": clientIp,
        "urls": urls,
    }
