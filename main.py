import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from api import notes
from db import engine, database, metadata

metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
