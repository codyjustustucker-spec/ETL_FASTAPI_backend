import sqlite3
from fastapi import APIRouter, HTTPException, status

from lso.api.schemas import SystemCreateRequest, SystemOut
from lso.db import queries

router = APIRouter(prefix="/systems", tags=["systems"])


@router.post("", response_model=SystemOut, status_code=status.HTTP_201_CREATED)
def create_system(payload: SystemCreateRequest) -> SystemOut:
    try:
        row = queries.create_system(payload.name.strip())
        return SystemOut.model_validate(row)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409, detail="System name already exists")


@router.get("", response_model=list[SystemOut])
def list_systems() -> list[SystemOut]:
    rows = queries.list_systems()
    return [SystemOut.model_validate(r) for r in rows]
