from typing import List
from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from api import crud
from api.models import NoteDB, NoteSchema
from db import SessionLocal

router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema):
    note_id = await crud.post(payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.get("/{id}/", response_model=NoteDB)
async def read_note(id: int = Path(..., gt=0),):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/", response_model=List[NoteDB])
async def read_all_notes():
    return await crud.get_all()


@router.put("/{id}/", response_model=NoteDB)
async def update_note(payload: NoteSchema, id: int = Path(..., gt=0),):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_id = await crud.put(id, payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete(id)

    return note


# Sync

@router.get("/sync/{id}/", response_model=NoteDB)
def read_note_sync(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0),
):
    note = crud.get_sync(db_session=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("/sync/", response_model=NoteDB, status_code=201)
def create_note_sync(*, db: Session = Depends(get_db), payload: NoteSchema):
    print(payload)
    note = crud.post_sync(db_session=db, payload=payload)
    return note
