"""Entry schemas for request/response validation."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.entry import EntryStatus, SeverityLevel, WorkflowState
from app.schemas.common import BaseSchema, TimestampMixin


# Symptom schemas
class EntrySymptomBase(BaseModel):
    """Base symptom schema."""
    description: str = Field(..., min_length=1, max_length=1000)
    order_index: int = Field(..., ge=0)
    symptom_type: Optional[str] = Field(None, max_length=100)


class EntrySymptomCreate(EntrySymptomBase):
    """Schema for creating a symptom."""
    pass


class EntrySymptomResponse(EntrySymptomBase, BaseSchema):
    """Response schema for symptom."""
    id: UUID
    entry_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Incident schemas
class EntryIncidentBase(BaseModel):
    """Base incident schema."""
    incident_id: str = Field(..., min_length=1, max_length=255)
    incident_source: str = Field(..., min_length=1, max_length=100)
    incident_url: Optional[str] = Field(None, max_length=1000)
    occurred_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class EntryIncidentCreate(EntryIncidentBase):
    """Schema for linking an incident."""
    pass


class EntryIncidentResponse(EntryIncidentBase, BaseSchema):
    """Response schema for incident."""
    id: UUID
    entry_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Entry schemas
class EntryBase(BaseModel):
    """Base entry schema."""
    title: str = Field(..., min_length=1, max_length=500)
    description: str = Field(..., min_length=1)
    severity: SeverityLevel
    root_cause: Optional[str] = None
    impact_summary: Optional[str] = None
    detection_method: Optional[str] = Field(None, max_length=255)


class EntryCreate(EntryBase):
    """Schema for creating an entry."""
    workflow_state: WorkflowState = WorkflowState.DRAFT
    status: EntryStatus = EntryStatus.ACTIVE
    created_by: str = Field(..., min_length=1)
    symptoms: Optional[List[EntrySymptomCreate]] = None
    incidents: Optional[List[EntryIncidentCreate]] = None


class EntryUpdate(BaseModel):
    """Schema for updating an entry."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, min_length=1)
    severity: Optional[SeverityLevel] = None
    workflow_state: Optional[WorkflowState] = None
    status: Optional[EntryStatus] = None
    updated_by: Optional[str] = Field(None, min_length=1)
    root_cause: Optional[str] = None
    impact_summary: Optional[str] = None
    detection_method: Optional[str] = Field(None, max_length=255)


class EntryResponse(EntryBase, TimestampMixin, BaseSchema):
    """Response schema for entry."""
    id: UUID
    workflow_state: WorkflowState
    status: EntryStatus
    created_by: str
    updated_by: Optional[str] = None
    merged_into_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    
    # Nested relationships
    symptoms: List[EntrySymptomResponse] = []
    incidents: List[EntryIncidentResponse] = []

    class Config:
        from_attributes = True


class EntryListResponse(BaseModel):
    """Response for entry list with minimal data."""
    id: UUID
    title: str
    severity: SeverityLevel
    workflow_state: WorkflowState
    created_at: datetime
    created_by: str
    
    class Config:
        from_attributes = True


class EntryFilter(BaseModel):
    """Filter parameters for entry queries."""
    workflow_state: Optional[WorkflowState] = None
    severity: Optional[SeverityLevel] = None
    status: Optional[EntryStatus] = None
    created_by: Optional[str] = None
    search: Optional[str] = None
