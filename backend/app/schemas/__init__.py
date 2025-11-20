"""
Pydantic schemas shared across API routes.
"""

from app.schemas.entry import (
    EntryCreate,
    EntryIncidentCreate,
    EntryIncidentResponse,
    EntryResponse,
    EntrySymptomCreate,
    EntrySymptomResponse,
    EntryTagCreate,
    EntryTagResponse,
    EntryUpdate,
)
from app.schemas.auth import (
    UserRole,
    UserRegister,
    UserLogin,
    Token,
    TokenData,
    UserResponse,
)
from app.schemas.tag import (
    TagCreate,
    TagResponse,
    TagUpdate,
)


# Re-export models for easier import
__all__ = [
    "EntryCreate",
    "EntryIncidentCreate",
    "EntryIncidentResponse",
    "EntryResponse",
    "EntrySymptomCreate",
    "EntrySymptomResponse",
    "EntryTagCreate",
    "EntryTagResponse",
    "EntryUpdate",
    "UserRole",
    "UserRegister",
    "UserLogin",
    "Token",
    "TokenData",
    "UserResponse",
    "TagCreate",
    "TagResponse",
    "TagUpdate",
]
