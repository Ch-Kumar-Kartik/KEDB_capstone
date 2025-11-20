"""Tag schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TagBase(BaseModel):
    """Base tag schema."""
    name: str = Field(..., max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    color: Optional[str] = Field(None, max_length=7, pattern=r'^#[0-9A-Fa-f]{6}$')


class TagCreate(TagBase):
    """Schema for creating a new tag."""
    pass


class TagUpdate(BaseModel):
    """Schema for updating a tag."""
    name: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    color: Optional[str] = Field(None, max_length=7, pattern=r'^#[0-9A-Fa-f]{6}$')


class TagResponse(TagBase):
    """Schema for tag response."""
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

