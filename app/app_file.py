import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ccass.infrastructure import api

FRONT_END_URL = os.getenv("FRONT_END_URL", "http://localhost:3000")

origins = [
    FRONT_END_URL
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api.router)
