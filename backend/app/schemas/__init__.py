"""
Pydantic schemas shared across API routes.
"""

from app.schemas.auth import (
    Token,
    TokenData,
    UserLogin,
    UserRegister,
    UserResponse,
    UserRole,
)
from app.schemas.common import BaseSchema, PaginatedResponse, PaginationParams, TimestampMixin
from app.schemas.entry import (
    EntryCreate,
    EntryFilter,
    EntryIncidentCreate,
    EntryIncidentResponse,
    EntryListResponse,
    EntryResponse,
    EntrySymptomCreate,
    EntrySymptomResponse,
    EntryUpdate,
)
from app.schemas.review import (
    ReviewCreate,
    ReviewDecision,
    ReviewParticipantCreate,
    ReviewParticipantResponse,
    ReviewResponse,
    ReviewUpdate,
    ReviewWithEntryResponse,
)
from app.schemas.solution import (
    SolutionCreate,
    SolutionResponse,
    SolutionStepCreate,
    SolutionStepResponse,
    SolutionStepUpdate,
    SolutionUpdate,
    SolutionWithEntryResponse,
)
from app.schemas.tag import EntryTagCreate, EntryTagResponse, TagCreate, TagResponse, TagUpdate


# Re-export models for easier import
__all__ = [
    # Common
    "BaseSchema",
    "TimestampMixin",
    "PaginationParams",
    "PaginatedResponse",
    # Auth
    "UserRole",
    "UserRegister",
    "UserLogin",
    "Token",
    "TokenData",
    "UserResponse",
    # Entry
    "EntryCreate",
    "EntryUpdate",
    "EntryResponse",
    "EntryListResponse",
    "EntryFilter",
    "EntrySymptomCreate",
    "EntrySymptomResponse",
    "EntryIncidentCreate",
    "EntryIncidentResponse",
    # Solution
    "SolutionCreate",
    "SolutionUpdate",
    "SolutionResponse",
    "SolutionWithEntryResponse",
    "SolutionStepCreate",
    "SolutionStepUpdate",
    "SolutionStepResponse",
    # Tag
    "TagCreate",
    "TagUpdate",
    "TagResponse",
    "EntryTagCreate",
    "EntryTagResponse",
    # Review
    "ReviewCreate",
    "ReviewUpdate",
    "ReviewResponse",
    "ReviewWithEntryResponse",
    "ReviewDecision",
    "ReviewParticipantCreate",
    "ReviewParticipantResponse",
]
