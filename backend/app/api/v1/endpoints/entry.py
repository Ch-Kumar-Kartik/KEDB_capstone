from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import entry as crud_entry
from app.schemas.entry import EntryCreate, EntryResponse, EntryUpdate

router = APIRouter()


@router.post("/", response_model=EntryResponse, status_code=status.HTTP_201_CREATED)
async def create_entry(
    entry: EntryCreate,
    db: AsyncSession = Depends(get_db),
    # In a real application, you'd get the user from an authentication system.
    # For this example, we'll hardcode a creator.
    current_user_id: str = "test_user", 
):
    """Create a new KEDB entry."""
    db_entry = await crud_entry.create_entry(db, entry=entry, created_by=current_user_id)
    return db_entry


@router.get("/{entry_id}", response_model=EntryResponse)
async def read_entry(
    entry_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve a KEDB entry by ID."""
    db_entry = await crud_entry.get_entry(db, entry_id=entry_id)
    if db_entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    return db_entry


@router.get("/", response_model=List[EntryResponse])
async def read_entries(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve multiple KEDB entries."""
    entries = await crud_entry.get_all_entries(db, skip=skip, limit=limit)
    return entries


@router.put("/{entry_id}", response_model=EntryResponse)
async def update_entry(
    entry_id: UUID,
    entry: EntryUpdate,
    db: AsyncSession = Depends(get_db),
    # In a real application, you'd get the user from an authentication system.
    # For this example, we'll hardcode an updater.
    current_user_id: str = "test_user",
):
    """Update an existing KEDB entry."""
    db_entry = await crud_entry.update_entry(db, entry_id=entry_id, entry_update=entry, updated_by=current_user_id)
    if db_entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    return db_entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entry(
    entry_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a KEDB entry."""
    db_entry = await crud_entry.delete_entry(db, entry_id=entry_id)
    if db_entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    return
