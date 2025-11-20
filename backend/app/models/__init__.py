"""Models package - import all models for Alembic autogenerate."""
from app.models.agent import AgentCall, AgentSession
from app.models.audit import AuditLog, SuggestionEvent
from app.models.base import Base
from app.models.embedding import EntryEmbedding, SolutionEmbedding
from app.models.entry import Entry, EntryIncident, EntrySymptom, EntryStatus, SeverityLevel, WorkflowState
from app.models.review import ParticipantRole, Review, ReviewParticipant, ReviewStatus
from app.models.solution import Solution, SolutionStep, SolutionType
from app.models.tag import EntryTag, Tag
from app.models.user import User, UserRole
from app.models.utility import Attachment, Prompt

# Re-export models for easier import
__all__ = [
    "Base",
    "AgentCall",
    "AgentSession",
    "AuditLog",
    "SuggestionEvent",
    "EntryEmbedding",
    "SolutionEmbedding",
    "Entry",
    "EntryIncident",
    "EntrySymptom",
    "EntryStatus",
    "SeverityLevel",
    "WorkflowState",
    "ParticipantRole",
    "Review",
    "ReviewParticipant",
    "ReviewStatus",
    "Solution",
    "SolutionStep",
    "SolutionType",
    "EntryTag",
    "Tag",
    "User",
    "UserRole",
    "Attachment",
    "Prompt",
]
