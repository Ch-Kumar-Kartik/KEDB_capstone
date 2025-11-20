"""CRUD operations for tags."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


async def get_tag(db: AsyncSession, tag_id: UUID) -> Optional[Tag]:
    """Get a tag by ID."""
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    return result.scalars().first()


async def get_tag_by_name(db: AsyncSession, name: str) -> Optional[Tag]:
    """Get a tag by name."""
    result = await db.execute(select(Tag).where(Tag.name == name))
    return result.scalars().first()


async def get_all_tags(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Tag]:
    """Get all tags with pagination."""
    result = await db.execute(select(Tag).offset(skip).limit(limit).order_by(Tag.name))
    return list(result.scalars().all())


async def create_tag(db: AsyncSession, tag_data: TagCreate) -> Tag:
    """Create a new tag."""
    tag = Tag(
        name=tag_data.name,
        category=tag_data.category,
        description=tag_data.description,
        color=tag_data.color
    )
    
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    
    return tag


async def update_tag(db: AsyncSession, tag_id: UUID, tag_data: TagUpdate) -> Optional[Tag]:
    """Update an existing tag."""
    tag = await get_tag(db, tag_id)
    
    if not tag:
        return None
    
    # Update only provided fields
    if tag_data.name is not None:
        tag.name = tag_data.name
    if tag_data.category is not None:
        tag.category = tag_data.category
    if tag_data.description is not None:
        tag.description = tag_data.description
    if tag_data.color is not None:
        tag.color = tag_data.color
    
    await db.commit()
    await db.refresh(tag)
    
    return tag


async def delete_tag(db: AsyncSession, tag_id: UUID) -> bool:
    """Delete a tag."""
    tag = await get_tag(db, tag_id)
    
    if not tag:
        return False
    
    await db.delete(tag)
    await db.commit()
    
    return True

