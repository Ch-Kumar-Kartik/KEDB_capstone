from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.entry import Entry, EntryIncident, EntrySymptom, EntryTag
from app.schemas.entry import EntryCreate, EntryUpdate


async def get_entry(db: AsyncSession, entry_id: UUID) -> Optional[Entry]:
    """Retrieve a single entry by its ID."""
    stmt = (
        select(Entry)
        .where(Entry.id == entry_id)
        .options(
            selectinload(Entry.symptoms),
            selectinload(Entry.incidents),
            selectinload(Entry.tags),
            selectinload(Entry.solutions),
            selectinload(Entry.reviews)
        )
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_entries(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Entry]:
    """Retrieve a list of all entries."""
    stmt = (
        select(Entry)
        .options(
            selectinload(Entry.symptoms),
            selectinload(Entry.incidents),
            selectinload(Entry.tags),
            selectinload(Entry.solutions),
            selectinload(Entry.reviews)
        )
        .offset(skip)
        .limit(limit)
        .order_by(Entry.created_at.desc())
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_entry(db: AsyncSession, entry: EntryCreate, created_by: str) -> Entry:
    """Create a new entry in the database."""
    db_entry = Entry(
        **entry.model_dump(exclude_unset=True, exclude={
            "symptoms", "incidents", "tags", "created_by"}),
        created_by=created_by,
    )
    
    # Handle relationships
    if entry.symptoms:
        for i, symptom_data in enumerate(entry.symptoms):
            db_entry.symptoms.append(EntrySymptom(**symptom_data.model_dump(), order_index=i))
    
    if entry.incidents:
        db_entry.incidents.extend([EntryIncident(**inc.model_dump()) for inc in entry.incidents])
        
    if entry.tags:
        db_entry.tags.extend([EntryTag(**tag.model_dump()) for tag in entry.tags])

    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry, ["symptoms", "incidents", "tags", "solutions", "reviews"])
    return db_entry


async def update_entry(db: AsyncSession, entry_id: UUID, entry_update: EntryUpdate, updated_by: str) -> Optional[Entry]:
    """Find an entry by ID and update its fields."""
    db_entry = await get_entry(db, entry_id)
    if db_entry:
        update_data = entry_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_entry, key, value)
        db_entry.updated_by = updated_by
        await db.commit()
        await db.refresh(db_entry)
    return db_entry


async def delete_entry(db: AsyncSession, entry_id: UUID) -> Optional[Entry]:
    """Remove an entry by its ID."""
    db_entry = await get_entry(db, entry_id)
    if db_entry:
        await db.delete(db_entry)
        await db.commit()
    return db_entry
