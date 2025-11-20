from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.entry import EntryStatus, SeverityLevel, WorkflowState


class EntrySymptomBase(BaseModel):
    description: str = Field(..., min_length=1)
    order_index: int = Field(..., ge=0)
    symptom_type: Optional[str] = None


class EntrySymptomCreate(EntrySymptomBase):
    pass


class EntrySymptomResponse(EntrySymptomBase):
    id: UUID
    entry_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class EntryIncidentBase(BaseModel):
    incident_id: str = Field(..., min_length=1)
    incident_source: str
    incident_url: Optional[str] = None
    occurred_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class EntryIncidentCreate(EntryIncidentBase):
    pass


class EntryIncidentResponse(EntryIncidentBase):
    id: UUID
    entry_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class EntryTagBase(BaseModel):
    name: str = Field(..., min_length=1)


class EntryTagCreate(EntryTagBase):
    pass


class EntryTagResponse(EntryTagBase):
    id: UUID
    entry_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class EntryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str = Field(..., min_length=1)
    severity: SeverityLevel
    workflow_state: WorkflowState = WorkflowState.DRAFT
    status: EntryStatus = EntryStatus.ACTIVE
    created_by: str = Field(..., min_length=1)
    root_cause: Optional[str] = None
    impact_summary: Optional[str] = None
    detection_method: Optional[str] = None


class EntryCreate(EntryBase):
    symptoms: Optional[List[EntrySymptomCreate]] = None
    incidents: Optional[List[EntryIncidentCreate]] = None
    tags: Optional[List[EntryTagCreate]] = None


class EntryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, min_length=1)
    severity: Optional[SeverityLevel] = None
    workflow_state: Optional[WorkflowState] = None
    status: Optional[EntryStatus] = None
    updated_by: Optional[str] = Field(None, min_length=1)
    root_cause: Optional[str] = None
    impact_summary: Optional[str] = None
    detection_method: Optional[str] = None
    # For simplicity, relationships are not updated directly via EntryUpdate in this example
    # but would typically have separate endpoints or more complex update logic.


class EntryResponse(EntryBase):
    id: UUID
    updated_by: Optional[str] = None
    merged_into_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    symptoms: List[EntrySymptomResponse] = []
    incidents: List[EntryIncidentResponse] = []
    tags: List[EntryTagResponse] = []

    class Config:
        from_attributes = True
