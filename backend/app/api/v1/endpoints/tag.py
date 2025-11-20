"""Tag management endpoints."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.crud import tag as crud_tag
from app.models.user import User
from app.schemas.tag import TagCreate, TagResponse, TagUpdate

router = APIRouter()


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new tag."""
    # Check if tag with same name already exists
    existing_tag = await crud_tag.get_tag_by_name(db, tag_data.name)
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tag with name '{tag_data.name}' already exists"
        )
    
    tag = await crud_tag.create_tag(db, tag_data)
    return tag


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a tag by ID."""
    tag = await crud_tag.get_tag(db, tag_id)
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    return tag


@router.get("/", response_model=List[TagResponse])
async def get_all_tags(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all tags."""
    tags = await crud_tag.get_all_tags(db, skip=skip, limit=limit)
    return tags


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: UUID,
    tag_data: TagUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a tag."""
    tag = await crud_tag.update_tag(db, tag_id, tag_data)
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a tag."""
    success = await crud_tag.delete_tag(db, tag_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    return None

